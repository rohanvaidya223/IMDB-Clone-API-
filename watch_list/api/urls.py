from django.urls import path
# from watch_list.api.views import movie_list,movie_details
from watch_list.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV,ReviewListAV, ReviewDetailAV,ReviewCreateAV,UserReview,WatchListAV,WatchList1
urlpatterns = [
   path('list/',WatchListAV.as_view(),name='watch_list'),
   path('<int:id>/',WatchDetailAV.as_view(),name='watch_detail'),
   path('stream/',StreamPlatformAV.as_view(),name='stream_platform'),
   path('stream/<int:id>/',StreamPlatformDetailAV.as_view(),name='stream_detail'),
   # path('review/',ReviewListAV.as_view(),name='review_list'),
   # path('review/<int:pk>',ReviewDetailAV.as_view(),name='review_detail'),
   path('<int:id>/reviews/',ReviewListAV.as_view(),name='review_list'),
   path('review/<int:pk>',ReviewDetailAV.as_view(),name='review_detail'),
   path('<int:id>/review-create/',ReviewCreateAV.as_view(),name='review_create'), 
   path('reviews/',UserReview.as_view(),name='user_review'),
   path('watchlist/',WatchList1.as_view(),name='watch_list1'),
   
   
]
