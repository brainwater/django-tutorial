from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.syndication.views import Feed

from polls.models import Choice, Poll

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

class MostPopularFeed(Feed):
    title = "Most Popular Polls Feed"
    link = "/polls/popular"
    description = "Ten Most Popular Polls"
    
    def items(self):
        objs = Poll.objects.all()
        # Sort the list based on the negative popularity
        return sorted(objs, key=lambda x: 0 - x.popularity())[:10]

    def item_title(self, item):
        return item.question

    def item_description(self, item):
        return item.choices_string()

    def item_link(self, item):
        return reverse('polls:detail', args=(item.id,))

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def like(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if (request.method == "POST"):
        p.likes += 1
        p.save()
    return render(request, 'polls/detail.html', { 'poll': p })

def likes(request, poll_id):
    return HttpResponse(Poll.objects.get(pk=poll_id).likes)
