from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.question
    def was_published_recently(self):
        now = timezone.now()
        return now > self.pub_date >= now - datetime.timedelta(days=1)
    def popularity(self):
        # Popularity is 5 times the number of likes plus the total number of votes
        numvotes = reduce(lambda y,z: y+z, map(lambda x: x.votes, self.choice_set.all()))
        return ( self.likes * 5 ) + numvotes
    def choices_string(self):
        # List choices with votes separated by commas
        return ', '.join([str(str(choice) + ': %d' % choice.votes) for choice in self.choice_set.all()])
    def num_write_in(self):
        the_choices = self.choice_set.all()
        write_in_choices = filter(lambda x: x.is_write_in, the_choices)
        write_in_votes = map(lambda y: y.votes, write_in_choices)
        return reduce(lambda z,a: a+z, write_in_votes)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    is_write_in = models.BooleanField(default=False)
    def __unicode__(self):
        return self.choice_text
