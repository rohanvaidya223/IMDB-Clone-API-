from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework import filters
# from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from watch_list.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from watch_list.api.serializers import WatchListSerializer, StreamPlatformSerializer,ReviewSerializer
from watch_list.models import WatchList, StreamPlatform,Review
from watch_list.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watch_list.api.pagination import WatchListPagination, WatchListLOPagination,WatchListCPagination


class UserReview(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)




class ReviewCreateAV(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle,AnonRateThrottle]

    def get_queryset(self):
        return Review.objects.all()
        
    
    def perform_create(self,serializer):
        id= self.kwargs.get('id')
        watchlist = WatchList.objects.get(id=id)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watch!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating= (watchlist.avg_rating+serializer.validated_data['rating'])/2
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)
        

class ReviewListAV(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        id = self.kwargs['id']
        return Review.objects.filter(watchlist=id)

class ReviewDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer  
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# class ReviewDetailAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewListAV(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class WatchList1(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^title', 'platform__name']
    #filter_backends = [filters.OrderingFilter]
    #ordering_fields = ['avg_rating']
    




class WatchListAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
        
    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class WatchDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request,id):
        try:
            movie = WatchList.objects.get(id=id)
        except WatchList.DoesNotExist:
            return Response({'Error': "Movie not found"},status = status.HTTP_404_NOT_FOUND)
            
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,id):
        movie = WatchList.objects.get(id=id)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id):
        movie = WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class StreamPlatformDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request,id):
        try:
            platform = StreamPlatform.objects.get(id=id)
        except StreamPlatform.DoesNotExist:
            return Response({"error":"Stream Platform Not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,id):
        platform = StreamPlatform.objects.get(id=id)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self,request,id):
        platform = StreamPlatform.objects.get(id=id)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)





# class ReviewListAV(APIView):
    
#     def get(self,request):
#         review = Review.objects.all()
#         serializer = ReviewSerializer(review, many=True)
#         return Response(serializer.data)































# @api_view(['GET','POST'])
# def movie_list(request):
    
#     if request.method =='GET':
    
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method =='POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,id):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(id=id)
#         except Movie.DoesNotExist:
#             return Response({'Error': "Movie not found"},status = status.HTTP_404_NOT_FOUND)
            
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method =='PUT':
#         movie = Movie.objects.get(id=id)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method =='DELETE':
#         movie = Movie.objects.get(id=id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    