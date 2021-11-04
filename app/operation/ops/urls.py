from django.urls import path
from .views import Ops

ops = Ops()

urlpatterns = [
    path('', ops.home, name='ops-home'),
    path('blocks/', ops.blocks, name='ops-blocks'),
    path('identities/', ops.identities, name='ops-identities'),
    path('get-raw', ops.getBlockRaw, name='ops-raw'),
    path('get-trans', ops.getTransactions, name='ops-trans'),
    path('chaincode/', ops.chaincode, name='ops-chaincode'),
    path('channels/', ops.chan, name='ops-channel'),
    path('new-channel', ops.new_channel, name='ops-new-channel'),
    path('join-channel', ops.join_channel, name='ops-join-channel'),
    # path('', ops.channels, name='ops-channels')
]