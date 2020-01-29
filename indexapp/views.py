from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import ImagePost
from .forms import PostUrlForm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from django.core.files import File
from autosnap import settings
import datetime
import hashlib
import pathlib
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def get_image(url, pic_path):
    # chromedriver的路径
    chromedriver = settings.CHROME_DRIVE
    os.environ["webdriver.chrome.driver"] = chromedriver
    # 设置chrome开启的模式，headless就是无界面模式
    # 一定要使用这个模式，不然截不了全页面，只能截到你电脑的高度
    chrome_options = Options()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    # 控制浏览器写入并转到链接
    driver.get(url)
    time.sleep(1)
    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    title = driver.execute_script("return document.title")
    filename = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()+".png"
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)
    time.sleep(1)
    # 截图并关掉浏览器
    driver.save_screenshot(os.path.join(pic_path, filename))
    driver.close()
    return title, filename


def index(request):
    if request.method == 'POST':
        posted = False
        form = PostUrlForm(request.POST)
        if form.is_valid():
            url = form.data.get("url")
            url_hash = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()

            post_count = ImagePost.objects.filter(url_hash=url_hash).count()
            print(post_count)
            if post_count > 0:
                exist_post = ImagePost.objects.get(url_hash=url_hash)
                return HttpResponseRedirect(reverse('indexapp:detail', args=(exist_post.id,)))

            now = datetime.datetime.now()
            relative_path = os.path.join('snapshot', str(now.year), str(now.month), str(now.day))
            image_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)

            img_info = get_image(url, image_path)
            post = ImagePost(page_title=img_info[0],
                             image_path=os.path.join(relative_path, img_info[1]),
                             url=url,
                             url_hash=url_hash)
            post.save()
            return HttpResponseRedirect(reverse('indexapp:detail', args=(post.id,)))

    else:
        form = PostUrlForm(initial={})
        posted = True

    return render(request, 'index.html', {'form': form, 'posted': posted})


def detail(request, page_id):
    page = get_object_or_404(ImagePost, pk=page_id)
    return render(request, 'detail.html', {'page': page})


class PageListView(generic.ListView):
    template_name = 'list.html'
    context_object_name = 'page_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return ImagePost.objects.all()
