# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

from models import *

ENDPOINTS = {
	'mentions': {
		'endpoint': "statuses/mentions_timeline.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['count', 'since_id', 'max_id', 'trim_user', 'contributor_details', 'include_entities'],
		'model': StatusCollection,
	},
	'user_timeline': {
		'endpoint': "statuses/user_timeline.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'since_id', 'count', 'max_id', 'trim_user', 'exclude_replies', 'contributor_details', 'include_rts'],
		'model': StatusCollection,
	},
	'home_timeline': {
		'endpoint': "statuses/home_timeline.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['count', 'since_id', 'max_id', 'trim_user', 'exclude_replies', 'contributor_details', 'include_entities'],
		'model': StatusCollection,
	},
	'retweets_of_me': {
		'endpoint': "statuses/retweets_of_me.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['count', 'since_id', 'max_id', 'trim_user', 'include_entities', 'include_user_entities'],
		'model': StatusCollection,
	},
	'retweets': {
		'endpoint': "statuses/retweets/%s.json",
		'post': False,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': ['count', 'trim_user'],
		'model': StatusCollection,
	},
	'get_status': {
		'endpoint': "statuses/show/%s.json",
		'post': False,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': ['trim_user', 'include_my_retweet', 'include_entities'],
		'model': Status,
	},
	'delete_status': {
		'endpoint': "statuses/destroy/%s.json",
		'post': True,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': ['trim_user'],
		'model': Status,
	},
	'update_status': {
		'endpoint': "statuses/update.json",
		'post': True,
		'url_params': [],
		'required_params': ['status'],
		'optional_params': ['in_reply_to_status_id', 'lat', 'long', 'place_id', 'display_coordinates', 'trim_user'],
		'model': Status,
	},
	'retweet': {
		'endpoint': "statuses/retweet/%s.json",
		'post': True,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': ['trim_user'],
		'model': Status,
	},
	'update_status_with_media': {
		'endpoint': "statuses/update_with_media.json",
		'post': True,
		'url_params': [],
		'required_params': ['status', 'media[]'],
		'optional_params': ['possibly_sensitive', 'in_reply_to_status_id', 'lat', 'long', 'place_id', 'display_coordinates'],
		'model': Status,
	},
	'update_status_with_multiple_media': {
		'endpoint': "statuses/update.json",
		'post': True,
		'url_params': [],
		'required_params': ['status', 'media'],
		'optional_params': ['in_reply_to_status_id', 'lat', 'long', 'place_id', 'display_coordinates', 'trim_user'],
		'model': Status,
	},
	'oembed': {
		'endpoint': "statuses/oembed.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['id', 'url', 'maxwidth', 'hide_media', 'hide_thread', 'omit_script', 'align', 'related', 'lang'],
		'model': OEmbed,
	},
	'search_tweets': {
		'endpoint': "search/tweets.json",
		'post': False,
		'url_params': [],
		'required_params': ['q'],
		'optional_params': ['geocode', 'lang', 'locale', 'result_type', 'count', 'until', 'since_id', 'max_id', 'include_entities'],
		'model': SearchResult,
	},
	'received_messages': {
		'endpoint': "direct_messages.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['since_id', 'max_id', 'count', 'page', 'include_entities', 'skip_status'],
		'model': MessageCollection,
	},
	'sent_messages': {
		'endpoint': "direct_messages/sent.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['since_id', 'max_id', 'count', 'page', 'include_entities'],
		'model': MessageCollection,
	},
	'get_message': {
		'endpoint': "direct_messages/show.json",
		'post': False,
		'url_params': [],
		'required_params': ['id'],
		'optional_params': [],
		'model': Message,
	},
	'delete_message': {
		'endpoint': "direct_messages/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': ['id'],
		'optional_params': ['include_entities'],
		'model': Message,
	},
	'send_message': {
		'endpoint': "direct_messages/new.json",
		'post': True,
		'url_params': [],
		'required_params': ['text'],
		'optional_params': ['user_id', 'screen_name'],
		'model': Message,
	},
	'no_retweets_ids': {
		'endpoint': "friendships/no_retweets/ids.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['stringify_ids'],
		'model': None,
	},
	'friends_ids': {
		'endpoint': "friends/ids.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'cursor', 'stringify_ids'],
		'model': CursoredIDCollection,
	},
	'followers_ids': {
		'endpoint': "followers/ids.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'cursor', 'stringify_ids'],
		'model': CursoredIDCollection,
	},
	'get_friendships': {
		'endpoint': "friendships/lookup.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id'],
		'model': SimpleRelationshipCollection,
	},
	'received_follower_requests': {
		'endpoint': "friendships/incoming.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['cursor', 'stringify_ids'],
		'model': CursoredIDCollection,
	},
	'sent_follower_requests': {
		'endpoint': "friendships/outgoing.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['cursor', 'stringify_ids'],
		'model': CursoredIDCollection,
	},
	'follow': {
		'endpoint': "friendships/create.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id', 'follow'],
		'model': User,
	},
	'unfollow': {
		'endpoint': "friendships/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id'],
		'model': User,
	},
	'update_friendship': {
		'endpoint': "friendships/update.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id', 'device', 'retweets'],
		'model': Relationship,
	},
	'get_friendship': {
		'endpoint': "friendships/show.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['source_id', 'source_screen_name', 'target_id', 'target_screen_name'],
		'model': Relationship,
	},
	'friends': {
		'endpoint': "friends/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'cursor', 'skip_status', 'include_user_entities'],
		'model': CursoredUserCollection,
	},
	'followers': {
		'endpoint': "followers/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'cursor', 'skip_status', 'include_user_entities'],
		'model': CursoredUserCollection,
	},
	'get_settings': {
		'endpoint': "account/settings.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': Settings,
	},
	'verify_credentials': {
		'endpoint': "account/verify_credentials.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['include_entities', 'skip_status'],
		'model': User,
	},
	'update_settings': {
		'endpoint': "account/settings.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['trend_location_woeid', 'sleep_time_enabled', 'start_sleep_time', 'end_sleep_time', 'time_zone', 'lang'],
		'model': Settings,
	},
	'update_delivery_device': {
		'endpoint': "account/update_delivery_device.json",
		'post': True,
		'url_params': [],
		'required_params': ['device'],
		'optional_params': ['include_entities'],
		'model': None,
	},
	'update_profile': {
		'endpoint': "account/update_profile.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['name', 'url', 'location', 'description', 'include_entities', 'skip_status'],
		'model': User,
	},
	'update_background': {
		'endpoint': "account/update_profile_background_image.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['image', 'tile', 'include_entities', 'skip_status', 'use'],
		'model': User,
	},
	'update_colors': {
		'endpoint': "account/update_profile_colors.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['profile_background_color', 'profile_link_color', 'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color', 'include_entities', 'skip_status'],
		'model': User,
	},
	'update_profile_image': {
		'endpoint': "account/update_profile_image.json",
		'post': True,
		'url_params': [],
		'required_params': ['image'],
		'optional_params': ['include_entities', 'skip_status'],
		'model': User,
	},
	'blocks': {
		'endpoint': "blocks/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['include_entities', 'skip_status', 'cursor'],
		'model': CursoredUserCollection,
	},
	'blocks_ids': {
		'endpoint': "blocks/ids.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['stringify_ids', 'cursor'],
		'model': CursoredIDCollection,
	},
	'block': {
		'endpoint': "blocks/create.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id', 'include_entities', 'skip_status'],
		'model': User,
	},
	'unblock': {
		'endpoint': "blocks/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id', 'include_entities', 'skip_status'],
		'model': User,
	},
	'get_users': {
		'endpoint': "users/lookup.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id', 'include_entities'],
		'model': UserCollection,
	},
	'get_user': {
		'endpoint': "users/show.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'include_entities'],
		'model': User,
	},
	'search_users': {
		'endpoint': "users/search.json",
		'post': False,
		'url_params': [],
		'required_params': ['q'],
		'optional_params': ['page', 'count', 'include_entities'],
		'model': UserCollection,
	},
	'get_contributees': {
		'endpoint': "users/contributees.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'include_entities', 'skip_status'],
		'model': UserCollection,
	},
	'get_contributors': {
		'endpoint': "users/contributors.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'include_entities', 'skip_status'],
		'model': UserCollection,
	},
	'remove_profile_banner': {
		'endpoint': "account/remove_profile_banner.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': None,
	},
	'update_profile_banner': {
		'endpoint': "account/update_profile_banner.json",
		'post': True,
		'url_params': [],
		'required_params': ['banner'],
		'optional_params': ['width', 'height', 'offset_left', 'offset_top'],
		'model': None,
	},
	'get_profile_banner': {
		'endpoint': "users/profile_banner.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name'],
		'model': Sizes,
	},
	'get_suggestion_category': {
		'endpoint': "users/suggestions/%s.json",
		'post': False,
		'url_params': ['slug'],
		'required_params': [],
		'optional_params': ['lang'],
		'model': Category,
	},
	'get_suggestion_categories': {
		'endpoint': "users/suggestions.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['lang'],
		'model': CategoryCollection,
	},
	'suggested_users': {
		'endpoint': "users/suggestions/%s/members.json",
		'post': False,
		'url_params': ['slug'],
		'required_params': [],
		'optional_params': [],
		'model': UserCollection,
	},
	'favorites': {
		'endpoint': "favorites/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'count', 'since_id', 'max_id', 'include_entities'],
		'model': StatusCollection,
	},
	'unfavorite': {
		'endpoint': "favorites/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': ['id'],
		'optional_params': ['include_entities'],
		'model': Status,
	},
	'favorite': {
		'endpoint': "favorites/create.json",
		'post': True,
		'url_params': [],
		'required_params': ['id'],
		'optional_params': ['include_entities'],
		'model': Status,
	},
	'lists': {
		'endpoint': "lists/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name'],
		'model': ListCollection,
	},
	'list_timeline': {
		'endpoint': "lists/statuses.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'owner_screen_name', 'owner_id', 'since_id', 'max_id', 'count', 'include_entities', 'include_rts'],
		'model': StatusCollection,
	},
	'remove_from_list': {
		'endpoint': "lists/members/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'user_id', 'screen_name', 'owner_screen_name', 'owner_id'],
		'model': List,
	},
	'list_memberships': {
		'endpoint': "lists/memberships.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'cursor', 'filter_to_owned_lists'],
		'model': CursoredListCollection,
	},
	'list_subscribers': {
		'endpoint': "lists/subscribers.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'owner_screen_name', 'owner_id', 'cursor', 'include_entities', 'skip_status'],
		'model': CursoredUserCollection,
	},
	'follow_list': {
		'endpoint': "lists/subscribers/create.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['owner_screen_name', 'owner_id', 'list_id', 'slug'],
		'model': List,
	},
	'user_follows_list': {
		'endpoint': "lists/subscribers/show.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['owner_screen_name', 'owner_id', 'list_id', 'slug', 'user_id', 'screen_name', 'include_entities', 'skip_status'],
		'model': User,
	},
	'unfollow_list': {
		'endpoint': "lists/subscribers/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['owner_screen_name', 'owner_id', 'list_id', 'slug'],
		'model': List,
	},
	'batch_add_to_list': {
		'endpoint': "lists/memberships/create_all.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'user_id', 'screen_name', 'owner_screen_name', 'owner_id'],
		'model': None,
	},
	'user_in_list': {
		'endpoint': "list/members/show.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'user_id', 'screen_name', 'owner_screen_name', 'owner_id', 'include_entities'],
		'model': User,
	},
	'list_members': {
		'endpoint': "lists/members.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'owner_screen_name', 'owner_id', 'cursor', 'include_entities', 'skip_status'],
		'model': CursoredUserCollection,
	},
	'add_to_list': {
		'endpoint': "lists/members/create.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'user_id', 'screen_name', 'owner_screen_name', 'owner_id'],
		'model': List,
	},
	'delete_list': {
		'endpoint': "lists/destroy.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['owner_screen_name', 'owner_id', 'list_id', 'slug'],
		'model': List,
	},
	'update_list': {
		'endpoint': "lists/update.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'name', 'mode', 'description', 'owner_screen_name', 'owner_id'],
		'model': List,
	},
	'create_list': {
		'endpoint': "lists/create.json",
		'post': True,
		'url_params': [],
		'required_params': ['name'],
		'optional_params': ['mode', 'description'],
		'model': List,
	},
	'get_list': {
		'endpoint': "lists/show.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'owner_screen_name', 'owner_id'],
		'model': List,
	},
	'subscribed_lists': {
		'endpoint': "lists/subscriptions.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['user_id', 'screen_name', 'count', 'cursor'],
		'model': CursoredListCollection,
	},
	'batch_remove_from_list': {
		'endpoint': "lists/memberships/destroy_all.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['list_id', 'slug', 'user_id', 'screen_name', 'owner_screen_name', 'owner_id'],
		'model': None,
	},
	'saved_searches': {
		'endpoint': "saved_searches/list.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': SavedSearchCollection,
	},
	'get_saved_search': {
		'endpoint': "saved_searches/show/%s.json",
		'post': False,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': [],
		'model': SavedSearch,
	},
	'create_saved_search': {
		'endpoint': "saved_searches/create.json",
		'post': True,
		'url_params': [],
		'required_params': ['query'],
		'optional_params': [],
		'model': SavedSearch,
	},
	'delete_saved_search': {
		'endpoint': "saved_searches/destroy/%s.json",
		'post': True,
		'url_params': ['id'],
		'required_params': [],
		'optional_params': [],
		'model': SavedSearch,
	},
	'get_place': {
		'endpoint': "geo/id/%s.json",
		'post': False,
		'url_params': ['place_id'],
		'required_params': [],
		'optional_params': [],
		'model': Place,
	},
	'reverse_geocode': {
		'endpoint': "geo/reverse_geocode.json",
		'post': False,
		'url_params': [],
		'required_params': ['lat', 'long'],
		'optional_params': ['accuracy', 'granularity', 'max_results'],
		'model': PlaceSearchResult,
	},
	'search_places': {
		'endpoint': "geo/search.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['lat', 'long', 'query', 'ip', 'granularity', 'accuracy', 'max_results', 'contained_within'],
		'model': PlaceSearchResult,
	},
	'similar_places': {
		'endpoint': "geo/similar_places.json",
		'post': False,
		'url_params': [],
		'required_params': ['lat', 'long', 'name'],
		'optional_params': ['contained_within'],
		'model': PlaceSearchResult,
	},
	'create_place': {
		'endpoint': "geo/place.json",
		'post': True,
		'url_params': [],
		'required_params': ['name', 'contained_within', 'token', 'lat', 'long'],
		'optional_params': [],
		'model': Place,
	},
	'trends': {
		'endpoint': "trends/place.json",
		'post': False,
		'url_params': [],
		'required_params': ['id'],
		'optional_params': ['exclude'],
		'model': Trends,
	},
	'trend_locations': {
		'endpoint': "trends/available.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': TrendLocationCollection,
	},
	'closest_trend_locations': {
		'endpoint': "trends/closest.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['lat', 'long'],
		'model': TrendLocationCollection,
	},
	'report_spam': {
		'endpoint': "users/report_spam.json",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['screen_name', 'user_id'],
		'model': User,
	},
	'configuration': {
		'endpoint': "help/configuration.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': APIConfiguration,
	},
	'languages': {
		'endpoint': "help/languages.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': LanguageCollection,
	},
	'privacy_policy': {
		'endpoint': "help/privacy.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': PrivacyPolicy,
	},
	'terms_of_service': {
		'endpoint': "help/tos.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': [],
		'model': TermsOfService,
	},
	'rate_limit_status': {
		'endpoint': "application/rate_limit_status.json",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['resources'],
		'model': RateLimitStatus,
	},
}

STREAM_ENDPOINTS = {
	'filter_stream': {
		'endpoint': "statuses/filter.json",
		'host': "stream.twitter.com",
		'post': True,
		'url_params': [],
		'required_params': [],
		'optional_params': ['follow', 'track', 'locations', 'stall_warnings', 'language', 'filter_level'],
	},
	'sample_stream': {
		'endpoint': "statuses/sample.json",
		'host': "stream.twitter.com",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['stall_warnings', 'language', 'filter_level'],
	},
	'firehose_stream': {
		'endpoint': "statuses/firehose.json",
		'host': "stream.twitter.com",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['count', 'stall_warnings', 'language', 'filter_level'],
	},
	'user_stream': {
		'endpoint': "user.json",
		'host': "userstream.twitter.com",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['stall_warnings', 'with', 'replies', 'track', 'locations', 'language'],
	},
	'site_stream': {
		'endpoint': "site.json",
		'host': "sitestream.twitter.com",
		'post': False,
		'url_params': [],
		'required_params': [],
		'optional_params': ['follow', 'stall_warnings', 'with', 'replies'],
	},
}
