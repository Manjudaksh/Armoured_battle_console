from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def player_login(request):
    if request.user.is_authenticated:
        return redirect("player_home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            if not user.is_active:
                messages.error(
                    request,
                    "Your account is inactive. Contact the administrator.",
                )
                return render(
                    request,
                    "accounts/login.html",
                )

            login(request, user)

            return redirect("player_home")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )




from forces.models import ForcePlayerAssignment


@login_required
def player_home(request):
    assignments = ForcePlayerAssignment.objects.filter(
        user=request.user,
        is_active=True,
    ).select_related(
        "force",
        "force__country",
    )

    if not assignments.exists():
        return render(
            request,
            "accounts/no_force_assignment.html",
        )

    from scenarios.models import Battle

    battles = Battle.objects.filter(
        status__in=[
            Battle.Status.PLANNED,
            Battle.Status.ORBAT_SETUP,
        ]
    ).select_related(
        "exercise",
    ).order_by(
        "-created_at",
    )

    return render(
        request,
        "accounts/player_home.html",
        {
            "assignments": assignments,
            "battles": battles,
        },
    )

@login_required
def player_logout(request):
    logout(request)
    return redirect("player_login")