from django.shortcuts import get_object_or_404
from api import models
from django.http import Http404
from rest_framework.views import APIView, Response


def item_serializer(item):
    data = item.data
    data['id'] = item.pk
    return data


class ApiResource(APIView):
    permission_classes = ()
    authentication_classes = ()

    def _get_resource(self, db_id, resource_name):
        database = get_object_or_404(models.Database, pk=db_id)
        return get_object_or_404(models.Resource, database=database, resource_name=resource_name)

    def get(self, request, db_id, resource_name):
        resource = self._get_resource(db_id, resource_name)
        items = resource.item_set.all()
        return Response([item_serializer(x) for x in items], 200)

    def post(self, request, db_id, resource_name):
        resource = self._get_resource(db_id, resource_name)
        item = models.Item.objects.create(resource=resource, data=request.data)
        return Response(item_serializer(item), 201)


class ApiResourceItem(APIView):
    permission_classes = ()
    authentication_classes = ()

    def _get_item(self, db_id, resource_name, pk):
        database = get_object_or_404(models.Database, pk=db_id)
        resource = get_object_or_404(models.Resource, database=database, resource_name=resource_name)
        return get_object_or_404(models.Item, pk=pk, resource=resource)

    def get(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        return Response(item_serializer(item), 200)

    def put(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        item.data.update(request.data)
        item.save()
        return Response(item_serializer(item), 200)

    def delete(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        item.delete()   
        return Response({}, 201)


class ApiSubResource(APIView):
    permission_classes = ()
    authentication_classes = ()

    def _get_resource(self, db_id, resource_name, pk, subresource_name):
        database = get_object_or_404(models.Database, pk=db_id)
        resource = get_object_or_404(models.Resource, database=database, resource_name=resource_name)
        parent = get_object_or_404(models.Item, pk=pk, resource=resource)
        sub_resource = get_object_or_404(models.Resource, database=database, resource_name=sub_resource_name)
        return resource, parent, sub_resource

    def get(self, request, db_id, resource_name, pk, subresource_name):
        resource, parent, sub_resource = self._get_resource(db_id, resource_name, pk, subresource_name)
        items = sub_resource.item_set.all()
        return Response([item_serializer(x) for x in items if x.data.get(resource.fk_name, None) == parent], 200)

    def post(self, request, db_id, resource_name, pk, subresource_name):
        resource, parent, sub_resource = self._get_resource(db_id, resource_name, pk, subresource_name)
        data = request.data
        data[resource.fk_name] = parent.pk
        item = models.Item.objects.create(resource=sub_resource, data=data)
        return Response(item_serializer(item), 201)

class ApiSubResourceItem(APIView):
    permission_classes = ()
    authentication_classes = ()

    def _get_item(self, db_id, resource_name, pk):
        database = get_object_or_404(models.Database, pk=db_id)
        resource = get_object_or_404(models.Resource, database=database, resource_name=resource_name)
        parent = get_object_or_404(models.Item, pk=pk, resource=resource)
        sub_resource = get_object_or_404(models.Resource, database=database, resource_name=sub_resource_name)
        item = get_object_or_404(models.Item, pk=pk, resource=resource)
        if item.data.get(resource.fk_name, None) != parent.pk:
            raise Http404
        return item

    def get(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        return Response(item_serializer(item), 200)

    def put(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        item.data.update(request.data)
        item.save()
        return Response(item_serializer(item), 200)

    def delete(self, request, db_id, resource_name, pk):
        item = self._get_item(db_id, resource_name, pk)
        item.delete()   
        return Response({}, 201)
