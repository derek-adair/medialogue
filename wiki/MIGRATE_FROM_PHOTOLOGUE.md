# Why migrate to Medialogue?
**Video Support**: Using [django video encoding](https://github.com/escaped/django-video-encoding)
**Front end focus**: I've disregarded the admin UI for the end user. ;
1. Smooth upload experience.
2. Edit/upload/order media outside of admin UI
3. Thumbnails with easy_thumbnails

## Breaking Changes
1. Changed Gallery -> Album
2. I've removed the manyToMany relationship between media/albums.  I am now using [django-ordered-model](https://github.com/django-ordered-model/django-ordered-model) and a one to many relationship.  I'm mainly just attempting to mimick the UI/UX of facebook upload / media management.  This allowed me to integrate with [muuri](https://muuri.dev/).
3. Added some model inheritance.  Photo() and Video() iherit the Media() object.

# Migrating from Photologue
Maintaining data from [photologue](https://github.com/richardbarran/django-photologue) isn't exactly a straight forward process;
1. Your media cannot belong to more than one Album
2. Galleries are now Albums
3. Photos need to inherit from Media()

Currently, your best bet is to just do a data dump and then massage the export into the new data model(s).
