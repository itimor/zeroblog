from django.utils.deprecation import MiddlewareMixin


class CountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
        # try:
        #     count_nums = Counts.objects.get(id=1)
        #     count_nums.visit_nums += 1
        #     count_nums.save()
        # except Exception as e:
        #     Counts.objects.create(blog_nums=0, category_nums=0, tag_nums=0, visit_nums=0)
