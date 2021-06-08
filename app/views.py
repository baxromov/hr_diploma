# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.core import serializers
#
# from . import models
# from . import forms
#
#
# def index(request):
#     company = models.Company.objects.last()
#     context = {
#         'company': company
#     }
#     return render(request, 'app/page/index.html', context)
#
#
# def departments(request):
#     form = forms.NewCandidateForm()
#     if request.method == "POST":
#         form = forms.NewCandidateForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_staff = form.save(commit=False)
#             department_id = request.POST.get('department_id')
#             department = models.Department.objects.get(pk=department_id)
#             new_staff.department = department
#             new_staff.save()
#             questions = models.Question.objects.filter(department_id=department_id)
#             for question in questions:
#                 answer = request.POST.get('dep_' + str(question.id))
#                 models.Answer.objects.create(
#                     candidate=new_staff,
#                     question=question,
#                     answer=answer
#                 )
#     department = models.Department.objects.all()
#     return render(request, 'app/page/newcondidate.html', {'form': form, 'department': department})
#
#
# def question(request, pk):
#     new_candidate, created = models.NewStaff.objects.get_or_create(id=pk)
#     models.Question.objects.filter(department__id=new_candidate.pk)
#     form = forms.AnswerModelForm()
#     if request.method == "POST":
#         form = forms.AnswerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('question')
#     context = {
#         'form': form,
#         'new_candidate': new_candidate,
#     }
#     return render(request, 'app/page/questionanswer.html', context)
#
#
# def ajax_dep(request):
#     if request.is_ajax():
#         department_id = request.GET.get('department_id')
#         questions = models.Question.objects.filter(department_id=department_id)
#         serializer_instance = serializers.serialize('json', queryset=questions)
#         return JsonResponse({"questions": serializer_instance}, status=200)
#     return JsonResponse({"error": "Asdasd"}, status=400)
