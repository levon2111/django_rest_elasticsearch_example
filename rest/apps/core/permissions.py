#!/usr/bin/env python
# coding=utf-8
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class SelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, user):
        return request.method in permissions.SAFE_METHODS or user == request.user
