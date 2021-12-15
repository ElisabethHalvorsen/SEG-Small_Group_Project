"""User related views."""
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clubs.models import User, Member

@login_required
def show_user(request, user_id):
    """View that shows individual user details."""
    current_user = request.user
    try:
        members = Member.objects.filter(current_user = current_user)
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_user.html', {'user': user, 'myclubs':members})