from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest
from expshare import models
from django.views.decorators.csrf import csrf_protect
from expshare import util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from expshare import settings
from haystack.views import SearchView


#搜索
class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        context['category'] = models.CategoryModel.objects.all()
        return context


def direct(request, template):
    print('模板：{0}'.format(template))
    try:
        return render(request, '/' + template)
    except Exception as e:
        return render(request, '/404.html')


'''
首页
'''


class IndexView(TemplateView):
    template_name = 'expshare/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['category'] = models.CategoryModel.objects.all()

        share_list = models.ExpModel.objects.all().order_by('viewnum').reverse()
        pagenator = Paginator(share_list, settings.PAGE_SIZE)

        # 返回的page对象
        page = None
        page_url = '/index/'

        # 页码
        page_num = self.request.GET.get('page')
        try:
            if page_num:
                page = pagenator.get_page(page_num)
            else:
                page = pagenator.get_page(1)
        except PageNotAnInteger as e1:
            page = pagenator.get_page(1)

        context['page'] = page
        context['page_url'] = page_url
        context['category_name'] = u'热门'
        return context


'''新建分类跳转'''


def newcategory(request):
    return render(request, 'expshare/newcategory.html', locals())


'''添加分类'''


def addcategory(request):
    name = ''
    if request.method == 'POST':
        name = request.POST.get('name')
    else:
        name = request.GET.get('name')
    try:
        dic = util.addCurrentTime({})
        dic['name'] = name
        dic['viewnum'] = 0
        dic['createuser'] = 'jinfanx'
        dic['updateuser'] = 'jinfanx'
        models.CategoryModel.objects.create(**dic)
        return HttpResponse(u'添加成功')
    except Exception as e:
        raise e
        return HttpResponse(u'添加失败' + e.__str__(), )


'''新建分享跳转'''


def newshare(request):
    category = models.CategoryModel.objects.all()
    return render(request, 'expshare/newshare.html', locals(), {'category': category})


'''新建分享'''


def addshare(request):
    req = request.POST
    if request.method == 'GET':
        req = request.GET
    dic = util.addCurrentTime({})
    dic['category'] = models.CategoryModel.objects.get(id=req.get('category'))
    dic['keywords'] = req.get('keywords')
    dic['problem'] = req.get('problem')
    dic['reason'] = req.get('reason')
    dic['resolve'] = req.get('resolve')
    dic['viewnum'] = 0
    dic['createuser'] = 'jinfanx'
    dic['updateuser'] = 'jinfanx'
    # for k in dic:
    #     print("{0}={1}".format(k,dic[k]))
    try:
        models.ExpModel.objects.create(**dic)
        return HttpResponse("添加成功！")
    except Exception as e:
        return HttpResponse("添加失败！" + e.__str__())


'''分类浏览'''


def list_shares(request, category):
    c = models.CategoryModel.objects.get(id=category)
    share_list = models.ExpModel.objects.all().filter(category=c).order_by('viewnum').reverse()
    pagenator = Paginator(share_list, settings.PAGE_SIZE)

    # 返回的page对象
    page = None
    page_url = '/list_share/'+str(category)+'/'

    # 页码
    page_num = request.GET.get("page")
    try:
        if page_num:
            page = pagenator.get_page(page_num)
        else:
            page = pagenator.get_page(1)
    except PageNotAnInteger as e1:
        page = pagenator.get_page(1)

    category_list = models.CategoryModel.objects.all()

    return render(request,'expshare/index.html',{'page':page,'category':category_list,'page_url':page_url,'category_name':c.name})

def search(request):
    req = request.POST
    if request.method=='GET':
        req = request.GET

    kws = req.get('keywords')


    share_list = models.ExpModel.objects.all().filter(category=c).order_by('viewnum').reverse()
    pagenator = Paginator(share_list, settings.PAGE_SIZE)

    # 返回的page对象
    page = None
    page_url = '/list_share/' + str(category) + '/'

    # 页码
    page_num = request.GET.get("page")
    try:
        if page_num:
            page = pagenator.get_page(page_num)
        else:
            page = pagenator.get_page(1)
    except PageNotAnInteger as e1:
        page = pagenator.get_page(1)

    category_list = models.CategoryModel.objects.all()

    return render(request, 'expshare/index.html',
                  {'page': page, 'category': category_list, 'page_url': page_url, 'category_name': '搜索结果'})

class GoRegisterView(TemplateView):
    template_name = 'expshare/auth/register.html'