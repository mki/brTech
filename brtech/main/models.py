import mongoengine as mongo

mongo.connect('brtech')

class Country(mongo.Document):
    name_eu = mongo.StringField(max_length = 200, primary_key=True)
    name_ru = mongo.StringField(max_length = 200)
    slug = mongo.StringField(max_length = 200, unique=True)

    def __repr__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return self.name_eu


class City(mongo.Document):
    name_eu = mongo.StringField(max_length = 200, primary_key=True)
    name_ru = mongo.StringField(max_length = 200)
    slug = mongo.StringField(max_length = 200, unique=True)
    country = mongo.ReferenceField(Country)

    def __repr__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return self.name_eu


class Airport(mongo.Document):
    name_eu = mongo.StringField(max_length = 200)
    name_ru = mongo.StringField(max_length = 200)

    location = mongo.GeoPointField()

    altitude = mongo.IntField()

    timezone = mongo.FloatField()

    dst = mongo.StringField(max_length=1)

    slug = mongo.StringField(max_length = 200, unique=True)
    city = mongo.ReferenceField(City)

    def __unicode__(self):
        return u"%s, %s" % (self.name_eu, self.city)
