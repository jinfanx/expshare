from expshare.models import ExpModel
from haystack import indexes


class ExpModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ExpModel

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(state=2).exclude(state=3).order_by('-viewnum')
