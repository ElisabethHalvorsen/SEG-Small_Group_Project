"""Club related views"""
from django.conf import settings
from django.contrib.auth import decorators
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect, render
from clubs.forms import ClubCreationForm
from clubs.helpers import valid_user_required
from django.contrib.auth.decorators import login_required
from clubs.models import Member, Club,Post
from clubs.user_types import UserTypes
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage,InvalidPage



@login_required
def show_club(request, club_id):
    """View that shows individual club details."""
    try:
        club = Club.objects.get(id=club_id)
        members = Member.objects.filter(
            Q(user_type = UserTypes.MEMBER, club_membership=club) |
            Q(user_type = UserTypes.OFFICER, club_membership=club) |
            Q(user_type = UserTypes.CLUB_OWNER, club_membership=club)
        )
        club_members = members.count()
        posts = Post.objects.filter(club_own_id=club_id).order_by('-id')
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        user = request.user
        myclubs = Member.objects.filter(current_user = user)
        user_type = None
        try:
            club_owner = Member.objects.get(Q(user_type = UserTypes.CLUB_OWNER, club_membership=club))
            user_membership = Member.objects.get(current_user = user, club_membership = club)
            user_type = user_membership.user_type
        except ObjectDoesNotExist:
            pass
        club_owner = Member.objects.get(Q(user_type = UserTypes.CLUB_OWNER, club_membership=club))
        user = club_owner.current_user
        paginator = Paginator(posts, 10)
        try:
            page_number = request.GET.get('page', '1')
            page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage, InvalidPage):
            page = paginator.page(1)
        return render(request, 'show_club.html', {'club': club, 'user_type': user_type, 'user':user, 'club_members': club_members, 'myclubs': myclubs, 'page':page})



@login_required
def create_club(request):
    """View that creates club."""
    user = request.user
    members = Member.objects.filter(current_user = user)
    if request.method == 'POST':
        form = ClubCreationForm(request.POST)
        if form.is_valid():
            club = form.save()
            Member.objects.create(
                user_type=UserTypes.CLUB_OWNER,
                current_user=user,
                club_membership=club
            )
            messages.add_message(request, messages.SUCCESS, "Club was created successfully!")
            return redirect('feed')
        return redirect('create_club')
    else:
        form = ClubCreationForm()
    return render(request, 'create_club.html', {'form': form, 'myclubs': members})


class ClubListView(LoginRequiredMixin, ListView):
    """View that shows a list of all clubs."""

    model = Club
    template_name = "club_list.html"
    context_object_name = "clubs"
    paginate_by = settings.CLUBS_PER_PAGE

    def get_queryset(self):
        """Return all clubs."""
        return Club.objects.all()

    def get_context_data(self, **kwargs):
        """Return context data, including new post form."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['myclubs'] = Member.objects.filter(current_user = user)
        return context

@login_required
def apply(request):
    """View that shows all clubs your not a member of"""
    user = request.user
    members = Member.objects.filter(current_user = user)
    clubset = set()
    clubs = Club.objects.all()
    for club in clubs:
        try:
            Member.objects.get(current_user=user, club_membership=club)
        except ObjectDoesNotExist:
            clubset.add(club)
    return render(request, 'apply.html', {'clubs': clubset, 'myclubs':members})