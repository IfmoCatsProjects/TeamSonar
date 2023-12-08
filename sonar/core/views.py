from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views import View
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.auth.models import User
from .models import Profile, Game, Collision
from django.conf import settings

def main(request):
    return render(request, 'core/index.html')

def collide(request):
    viewed_id = request.GET.get('viewed_id')
    rejected = request.GET.get('accept', False)
    viewed_user = get_object_or_404(Profile, id=viewed_id)

    if Collision.objects.create(user=request.user, viewed_user=viewed_user, rejected=rejected):
        return HttpResponse('OK')
    return HttpResponse('ERR')

class SuggestionsView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        current_user = Profile.objects.get(user=request.user)
        viewed_users = self.get_viewed_users(current_user)
        similar_profiles = self.get_similar_profiles(current_user, viewed_users)

        suggestions = self.get_suggestions(similar_profiles)

        result = self.format_suggestions(suggestions)
        return JsonResponse(result, safe=False)

    def get_viewed_users(self, current_user):
        cache_key = f'viewed_users_{current_user.user.id}'
        viewed_users = cache.get(cache_key)

        if viewed_users is None:
            viewed_users = Collision.objects.filter(user=current_user).values_list('viewed_user__user', flat=True)
            cache.set(cache_key, viewed_users, timeout=60 * 5)  # Кеш на 5 минут

        return viewed_users

    def get_similar_profiles(self, current_user, viewed_users):
        cache_key = f'similar_profiles_{current_user.user.id}'
        similar_profiles = cache.get(cache_key)

        if similar_profiles is None or len(similar_profiles) < 10:
            similar_profiles = (
                Profile.objects.filter(games__in=current_user.games.all())
                .exclude(user=current_user.user)
                .exclude(id__in=viewed_users)
            )[:10]  # Ограничение на 10 профилей
            cache.set(cache_key, similar_profiles, timeout=60 * 5)  # Кеш на 5 минут

        return similar_profiles

    def get_suggestions(self, similar_profiles):
        common_games = Game.objects.filter(profile__in=similar_profiles).distinct()
        suggestions = (
            User.objects.filter(profile__games__in=common_games)
            .exclude(id=self.request.user.id)
            .annotate(common_games=ArrayAgg('profile__games__name', distinct=True))
            .values('id', 'username', 'common_games', 'profile__description', 'profile__avatar')
        )
        return suggestions

    def format_suggestions(self, suggestions):
        result = []
        for user_data in suggestions:
            avatar_url = f"{settings.MEDIA_URL}{user_data['profile__avatar']}" if user_data['profile__avatar'] else None
            games = user_data['common_games']
            result.append({
                'id': user_data['id'],  # Добавляем идентификатор пользователя в результат
                'username': user_data['username'],
                'common_games': games,
                'description': user_data['profile__description'],
                'avatar_url': avatar_url
            })
        return result

