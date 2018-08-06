from django import template

register = template.Library()

def getValueFromDbItem(dataItem, strField):
    return getattr(dataItem, strField)

register.filter('getValueFromDbItem', getValueFromDbItem)
