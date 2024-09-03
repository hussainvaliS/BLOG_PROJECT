from django.shortcuts import render
from blogapp.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from taggit.models import Tag


# Create your views here.
def Post_list_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__name__in=[tag])

    paginator = Paginator(object_list=post_list, per_page=2)
    page_number = request.GET.get("page")
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    my_dict = {"post_list": post_list, "tag": tag}
    print(my_dict)
    return render(
        request=request, template_name="blogapp/post_list.html", context=my_dict
    )


class PostListView(ListView):
    model = Post
    Paginate_by = 2


# # def Post_detail_view(request,year,month,day,Post):
# # 	Post = get_object_or_404(Post,slug=post,status='published',publish_year=year,publish_month=month,publish_day=day)
# # 	my_dict = {'Post':Post}
# # 	return render(request = request, template_name = 'blogapp/post_detail.html',content = my_dict)

# def Post_detail_view(request):
# 	post_list1 = Post.objects.all()
# 	my_dict1 = {'post_list1':post_list1}
# 	print(my_dict1)
# 	return render(request = request, template_name = 'blogapp/post_detail.html',context=my_dict1)


from django.shortcuts import render, get_object_or_404
from blogapp.models import Post, Comment


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, publish__year=year, publish__month=month, publish__day=day
    )

    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()

    my_dict_1 = {"post": post, "form": form, "csubmit": csubmit, "comments": comments}
    return render(request, "blogapp/post_detail.html", my_dict_1)


from blogapp.forms import *
from django.core.mail import send_mail


def mail_send_view(request, id):
    post = get_object_or_404(Post, id=id, status="published")

    send = False
    if request.method == "POST":
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({})recommends to read"{}"'.format(
                cd["name"], cd["email"], post.title
            )

            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = "read the post at :\n{} \n\n {}'s comments:\n{}".format(
                post_url,
                cd["name"],
                cd["comments"],
            )

            # send_mail(subject,message,form_mail,recipient_list)
            send_mail(subject, message, "shussainvali44@gmail.com", [cd["to"]])
            send = True

    else:

        form = EmailSendForm()

    my_dict = {"form": form, "post": post, "send": send}

    return render(
        request=request, template_name="blogapp/sharebymail.html", context=my_dict
    )
