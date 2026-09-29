from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Submission, Choice


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        submission = Submission.objects.create(
            enrollment=request.user.enrollment_set.first()
        )

        selected_choices = []

        for key, value in request.POST.items():
            if key.startswith("question_"):
                try:
                    choice = Choice.objects.get(id=value)
                    selected_choices.append(choice)
                except Choice.DoesNotExist:
                    pass

        submission.choices.set(selected_choices)

        return redirect("show_exam_result", submission_id=submission.id)

    return redirect("course_details", course_id=course.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    score = 0
    total = 0

    for choice in submission.choices.all():
        total += choice.question.grade

        if choice.is_correct:
            score += choice.question.grade

    context = {
        "submission": submission,
        "score": score,
        "total": total,
    }

    return render(
        request,
        "exam_result.html",
        context
    )
