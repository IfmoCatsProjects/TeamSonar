from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Gamer, Collision
from django.conf import settings
from django.core.cache import cache

User = settings.AUTH_USER_MODEL


def main(request):
    return render(request, 'index.html')


def collide(request):
    viewed_id = request.GET.get('viewed_id')
    accepted = request.GET.get('accept') == 'true'
    maybe_match = get_object_or_404(Collision, viewed_user=request.user)
    if maybe_match:
        if maybe_match.accept:
            maybe_match.match = True
            return HttpResponse('OK')
    viewed_user = get_object_or_404(Gamer, id=viewed_id)
    Collision.objects.create(user=request.user, viewed_user=viewed_user.user, accepted=accepted)
    return HttpResponse('OK')


def get_matches(request):
    matches = Collision.objects.filter(user=request.user, match=True)
    result = []
    for match in matches:
        result.append(
            {
                'username': match.viewed_user.username
            }
        )
    return JsonResponse(result, safe=False)


class SuggestionsView(View):
    @staticmethod
    def get_viewed_users(user):
        viewed_users = Collision.objects.all().filter(user=user.user)
        res = [viewed_users.values_list('viewed_user_id')]
        return res

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        viewer = Gamer.objects.get(user=request.user)
        viewed_ids = self.get_viewed_users(viewer)
        cache_key = f'sims_{viewer.id}'
        sims = cache.get(cache_key)
        if not sims:
            sims = Gamer.objects.filter(
                games__in=viewer.games.all()
            ).exclude(
                user=request.user
            )

        sims = sims.exclude(user__id__in=viewed_ids)

        cache.set(cache_key, sims, timeout=300)

        sims2 = sims.annotate(
            common_games=ArrayAgg('games__name', distinct=True)
        ).values(
            'user__id', 'user__username', 'common_games', 'description', 'avatar'
        )

        result = []

        for user_data in sims2:
            avatar_url = None
            result.append({
                'id': user_data['user__id'],
                'username': user_data['user__username'],
                'common_games': user_data['common_games'],
                'description': user_data['description'],
                'avatar_url': avatar_url
            })

        return JsonResponse(result, safe=False)
