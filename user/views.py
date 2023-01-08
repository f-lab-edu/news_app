from rest_framework import viewsets
from rest_framework.response import Response

from django.db.models import Count, Q

from user.models import User
from user.serializers import UserSerializer

from topic.models import Topic

from weekUserTopic.serializer import WeekUserTopicSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 1.1. 그외 validation 체크
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # 1. 번호 존재 유무 체크
            if self.queryset.filter(phone=serializer.data.phone).exists():
                return Response(data={'detail': 'This user already has a profile'}, status=400)

            # 2. 카테고리 3개 선택
            # 3. 다른 카테고리 선택
            category1 = serializer.data.category1
            category2 = serializer.data.category2
            category3 = serializer.data.category3

            if category1 == category2 or category2 == category3 or category1 == category3:
                return Response(data={'detail: 서로 다른 카테고리를 선택해주세요.'}, status=400)

            # 4. 유저 저장
            serializer.save()
            # self.perform_create(serializer)

            # 5. 카테고리 별 빈도 가장 높은 토픽 선택
            # 토픽에 가서 토픽에 있는 선택한 카테고리 별 빈도수가 가장 높은 토픽 각 3개를 뽑아온다.
            topic_queryset = Topic.objects.all()
            category1_cnt = topic_queryset.filter(category=category1).values('category', 'name').annotate(
                category_cnt=Count('category')).order_by('category_cnt')[0]
            category2_cnt = topic_queryset.filter(category=category2).values('category', 'name').annotate(
                category_cnt=Count('category')).order_by('category_cnt')[0]
            category3_cnt = topic_queryset.filter(category=category3).values('category', 'name').annotate(
                category_cnt=Count('category')).order_by('category_cnt')[0]

            topic1 = category1_cnt['name']
            topic2 = category2_cnt['name']
            topic3 = category3_cnt['name']

            # 6. 주차별 유저 토픽 추가
            # 주차별 유저 토픽에 추가한다.

            week_user_topic_data = [
                {'topic': topic1, 'user': serializer.data.phone, 'weeks': 0},
                {'topic': topic2, 'user': serializer.data.phone, 'weeks': 0},
                {'topic': topic3, 'user': serializer.data.phone, 'weeks': 0},
            ]

            week_user_topic_serializer = WeekUserTopicSerializer(data=week_user_topic_data, many=True)
            if not week_user_topic_serializer.is_valid():
                return Response({'detail': 'is not valid'}, 400)

            # 7. 주차별 유저 토픽을 저장한다.
            week_user_topic_serializer.save()

            # user_news_serializer = UserNewsSerializer()
            # user_news_serializer.save()

            # api endpoint 밖 -> serializer -> User, UserNews(DB)

            # serializer()
            return Response(serializer.data, 200)
        else:
            return Response({'detail': 'is not valid'}, 400)
