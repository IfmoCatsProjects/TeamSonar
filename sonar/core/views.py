from django.contrib.postgres.aggregates import ArrayAgg
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.core.cache import cache
from .models import Profile, Collision


def main(request):
    return render(request, 'core/cards.html')


def matches(request):
    user_matches = get_viewed_users(Profile.objects.get(user=request.user))
    return render(request, 'core/matches.html', {'user_matches':user_matches})


def collide(request):
    viewed_id = request.GET.get('viewed_id')
    accepted = request.GET.get('accept') == 'true'
    viewed_user = get_object_or_404(Profile, id=viewed_id)

    Collision.objects.create(user=Profile.objects.get(user=request.user), viewed_user=viewed_user, accepted=accepted)
    return HttpResponse('OK')


def get_viewed_users(user_profile):
    viewed_users = Collision.objects.all().filter(user=user_profile)
    return viewed_users.values_list('viewed_user_id')


class SuggestionsView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth')
        current_profile = Profile.objects.get(user=request.user)
        viewed_users = get_viewed_users(current_profile)
        cache_key = f'sims_{current_profile.id}'
        sims = cache.get(cache_key)
        if sims is None:
            sims = Profile.objects.filter(
                games__in=current_profile.games.all()
            ).exclude(
                user=request.user
            )
            cache.set(cache_key, sims, timeout=60 * 15)

        sims = sims.exclude(
            user_id__in=viewed_users
        )

        cache.set(cache_key, sims, timeout=60 * 15)

        profiles = sims.annotate(
            common_games=ArrayAgg('games__name', distinct=True)
        ).values(
            'user__id',
            'user__username',
            'common_games',
            'description',
            'avatar'
        )

        res = []
        for user_data in profiles:
            avatar_url = None
            res.append({
                'id': user_data['user__id'],
                'username': user_data['user__username'],
                'common_games': user_data['common_games'],
                'description': user_data['description'],
                'avatar_url': avatar_url
            })

        return JsonResponse(res, safe=False)
