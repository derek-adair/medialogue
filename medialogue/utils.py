from django.template.defaultfilters import slugify
import itertools

import logging
logger = logging.getLogger(__name__)

def querydict_to_dict(query_dict):
    # request.POST only returns the first value in a list, this grabs it all
    # Lovingly stolen from: https://tinyurl.com/h6my82s6
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

def _generate_slug(title, obj):
    logger.info("utils.generate_slug called")
    slug_candidate = slug_original = slugify(title)
    num_found = 0
    for i in itertools.count(1):
        if not obj.objects.filter(slug=slug_candidate).exists():
            break
        num_found+=1
        slug_candidate = '{}-{}'.format(slug_original, i)
    return slug_candidate, num_found
