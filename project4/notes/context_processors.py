from.models import Category

def common(repuest):
    #テンプレートに毎回渡すデータ
    context = {
        'category_list':Category.objects.all(),
    }
    return context