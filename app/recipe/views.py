from django.shortcuts import render

# Create your views here.
"""
Views for the recipe APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe,Tag,Ingredient
from recipe import serializers

from rest_framework import viewsets,mixins


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer #uses this for the Create,Update and Delete endpoints
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self,qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]
    
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags= self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset=self.queryset
        if tags:
            tags_id = self._params_to_ints(tags)
            queryset=queryset.filter(tags__id__in=tags_id)
        if ingredients:
            ingredients_id = self._params_to_ints(ingredients)
            queryset=queryset.filter(ingredients__id__in=ingredients_id)
            
        return queryset.filter(user=self.request.user).order_by('-id').distinct()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer #this is used for listing the recipes
        return self.serializer_class
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class =serializers.TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    