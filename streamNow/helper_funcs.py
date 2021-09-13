def media_detail_helper(response, media_type, _id, context):
    context['media_type'] = media_type
    context['id'] = _id

    # media_type is TV
    if media_type == 'tv':
        context['name'] = response['name']
        context['num_of_episodes'] = response['number_of_episodes']
        context['num_of_seasons'] = response['number_of_seasons']
        context['release_date'] = response['first_air_date']
        context['runtime'] = None
        context['revenue'] = None
    # media_type is movie
    else:
        context['name'] = response['title']
        context['imdb_id'] = response['imdb_id']
        context['release_date'] = response['release_date']
        context['runtime'] = response['runtime']
        context['revenue'] = '${:,.2f}'.format(response['revenue'])

    context['overview'] = response['overview']
    context['poster_path'] = response['poster_path']
    context['backdrop_path'] = response['backdrop_path']
    context['popularity'] = response['popularity']
    context['vote_average'] = response['vote_average']
    context['genres'] = response['genres']
    context['production_companies'] = response['production_companies']

    if response['homepage']:
        context['homepage'] = response['homepage']
    if response['tagline']:
        context['tagline'] = response['tagline']

    return context