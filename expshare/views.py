from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from expshare import models
from django.views.decorators.csrf import csrf_protect
from expshare import util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from expshare import settings
from haystack.views import SearchView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as syslogin,logout as syslogout
from django.contrib.auth.decorators import login_required,permission_required
from .util import MailUtil,JsonUtil
from django.db.models import Q


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

@login_required(login_url='/go_login/')
# @permission_required('add_categorymodel')
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
        dic['createuser'] = request.user.username
        dic['updateuser'] = request.user.username
        models.CategoryModel.objects.create(**dic)
        return HttpResponse(JsonUtil.get_json_response('success','添加成功！'),content_type='application/json')
    except Exception as e:
        return HttpResponse(JsonUtil.get_json_response('fail',u'添加失败' + e.__str__()),content_type='application/json' )


'''新建分享跳转'''

@login_required(login_url='/go_login/')
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
    dic['createuser'] = request.user.username
    dic['updateuser'] = request.user.username
    # for k in dic:
    #     print("{0}={1}".format(k,dic[k]))
    try:
        models.ExpModel.objects.create(**dic)
        return HttpResponse(JsonUtil.get_json_response('success','添加成功'),content_type='application/json')
    except Exception as e:
        return HttpResponse(JsonUtil.get_json_response('fail',"添加失败！" + e.__str__()),content_type='application/json')


'''分类浏览'''


def list_shares(request, category):
    c = models.CategoryModel.objects.get(id=category)
    share_list = models.ExpModel.objects.all().filter(category=c).order_by('-viewnum')
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

# 注册跳转
class GoRegisterView(TemplateView):
    template_name = 'expshare/auth/register.html'

#注册
def register(request):
    req = request.POST
    if request.method=='GET':
        req = request.GET
    username = req.get('username')
    password = req.get('password')
    email = req.get('email')
    phone = req.get('phone')
    profession = req.get('profession')

    #用户未激活，需要点击邮件中的链接激活账户
    u = None
    try:
        u = User.objects.create_user(username,password=password,email=email,is_active=False)
        dic = {'user':u, 'phone':phone, 'profession': profession}
        models.UserExtends.objects.create(**dic)
    except Exception as e:
        return HttpResponse(JsonUtil.get_json_response('fail','添加用户失败'+e.__str__()),content_type='application/json')
    #发邮件
    try:
        MailUtil.send_register_email(email,u)
    except Exception as e:
        e.with_traceback()
        return HttpResponse(JsonUtil.get_json_response('fail','邮件发送失败！'+e.__str__()),content_type='application/json')
    return HttpResponse(JsonUtil.get_json_response('success','注册成功，邮件确认即可完成注册！'),content_type='application/json')

def active_acct(request,userid,code):
    #编码校验
    c = models.MailRegisterCode.objects.filter(userid=userid).filter(code=code).count()
    if c==0:
        return render(request, 'expshare/auth/regsuccess.html', {'result': 'fail', 'msg': '账户激活失败！'})
    #激活邮件对应的账户
    try:
        u = User.objects.filter(id=userid).update(is_active=True)
    except Exception as e:
        return render(request, 'expshare/auth/regsuccess.html', {'result':'fail','msg':'账户激活失败！'+e.__str__()})

    return render(request,'expshare/auth/regsuccess.html',{'result':'success','msg':'注册成功！'})

def check_username(request):
    username = request.GET.get('username')
    count = User.objects.filter(username=username).count()
    if count>0:
        return HttpResponse(JsonUtil.get_json_response('fail','用户已存在'),content_type='application/json')
    else:
        return HttpResponse(JsonUtil.get_json_response('success','用户名可用'),content_type='application/json')

def check_email(request):
    email = request.GET.get('email')
    count = User.objects.filter(email=email).count()
    msg = '邮箱已注册'
    result = 'fail'
    if count==0:
        msg = '邮箱可用'
        result = 'success'
    return HttpResponse(JsonUtil.get_json_response(result,msg),content_type='application/json')

#登录跳转
def go_login(request):
    return render(request,'expshare/auth/login.html')

#登录
def login(request):
    req = request.POST
    if request.method=='GET':
        req = request.GET
    result = 'success'
    msg = '登录成功'

    username = req.get('username')
    password = req.get('password')
    #此处接收关键字参数，关键字不可省略
    user = authenticate(username=username,password=password)
    if user==None:
        user = User.objects.filter(Q(email=username)|Q(username=username))

        if user.count()==0:
            print('无用户名或邮箱对应的用户！'+username)
            result = 'fail'
            msg = '用户不存在！'
            return HttpResponse(JsonUtil.get_json_response(result,msg),content_type='application/json')
        else:
            # user = user[0]
            user = user.get()
            l = locals()
            user = authenticate(username=user.username,password=password)


    if user==None:
        result = 'fail'
        msg = '登录失败！用户名或密码错误'
    else:
        if user.is_active:
            syslogin(request,user)
        else:
            result = 'fail'
            msg = '账户未激活'
    return HttpResponse(JsonUtil.get_json_response(result,msg),content_type='application/json')

#注销
def logout(request):
    syslogout(request)
    return HttpResponseRedirect('/')

#我的笔记
@login_required(login_url='/go_login/')
def my_note(request):
    username = request.user.username
    share_list = models.ExpModel.objects.all().filter(createuser=username).order_by('-createdate')
    pagenator = Paginator(share_list, settings.PAGE_SIZE)

    # 返回的page对象
    page = None
    page_url = '/my_note/'

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

    return render(request,'expshare/index.html',{'page':page,'category':category_list,'page_url':page_url,'category_name':'我的笔记'})

#点赞 ajax
@login_required(login_url='/go_login/')
def praise(request):
    result = 'success'
    msg = '成功！'
    shareid = request.GET.get('shareid')

    #是否已经点赞过
    c = models.SharePraise.objects.filter(userid=request.user.id).filter(shareid=shareid).count()
    if c>0:
        result = 'fail'
        msg = '您已赞过！'
        return HttpResponse(JsonUtil.get_json_response(result, msg), content_type='application/json')

    share = models.ExpModel.objects.filter(id=shareid).get()
    share.viewnum += 1
    try:
        share.save()
        models.SharePraise.objects.create(userid=request.user.id,shareid=shareid)
    except Exception as e:
        msg = '失败'+e.__str__()
        result = 'fail'

    return HttpResponse(JsonUtil.get_json_response(result,msg),content_type='application/json')

def feedback(request):
    result = 'success'
    msg = '感谢反馈，反馈已成功！'
    req = request.GET

    dic = util.addCurrentTime({})
    dic['share'] = models.ExpModel.objects.get(id=req.get('shareid'))
    dic['createuser'] = request.user.id
    dic['updateuser'] = dic['createuser']
    dic['reason'] = req.get('reason')
    dic['type'] = req.get('type')
    try:
        models.Feedback.objects.create(**dic)
    except Exception as e:
        result = 'fail'
        msg = '反馈失败！'+e.__str__()
    return HttpResponse(JsonUtil.get_json_response(result,msg),content_type='application/json')
