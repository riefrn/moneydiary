from django.urls import path, re_path
import web.views
urlpatterns = [
    path('', web.views.index, name='index'),
    path('list-weekly-expenses/', web.views.listsweeklyexpenses,
         name='backoffice-list-weekly-expenses'),
    path('add-weekly-expenses/', web.views.addweeklyexpenses,
         name='backoffice-add-weekly-expenses'),
    re_path('edit-weekly-expenses/(?P<weekly_expenses_id>\d+)/',
            web.views.editweeklyexpenses, name='backoffice-edit-weekly-expenses'),
    path('delete-weekly-expenses/', web.views.deleteweeklyexpenses,
         name='backoffice-delete-weekly-expenses'),
    path('list-transaction/', web.views.liststransaction,
         name='backoffice-list-transaction'),
    path('add-transaction/', web.views.addtransaction,
         name='backoffice-add-transaction'),
    re_path('edit-transaction/(?P<transaction_id>\d+)/',
            web.views.edittransaction, name='backoffice-edit-transaction'),
    path('delete-transaction/', web.views.deletetransaction,
         name='backoffice-delete-transaction'),
    re_path('add-transaction-index/(?P<spending_id>\d+)/', web.views.addtransactionindex,
            name='backoffice-add-transaction-index'),
    path('list-period-transaction/', web.views.listperiodtransaction,
         name='backoffice-list-period-transaction'),
    path('list-transaction-period/', web.views.transactionperiod,
         name='backoffice-list-transaction-period'),
    path('delete-transaction-period/', web.views.deletetransactionperiod,
         name='backoffice-delete-transaction-period'),
    path('list-note/', web.views.listsnote,
         name='backoffice-list-note'),
    path('add-note/', web.views.addnote,
         name='backoffice-add-note'),
    re_path('edit-note/(?P<note_id>\d+)/',
            web.views.editnote, name='backoffice-edit-note'),
    path('delete-note/', web.views.deletenote,
         name='backoffice-delete-note'),
    path('chart-transaction/', web.views.charttransaction,
         name='backoffice-chart-transaction'),
    path('filter-weekly-expenses/', web.views.filterweeklyexpenses,
         name='backoffice-filter-weekly-expneses'),

]
