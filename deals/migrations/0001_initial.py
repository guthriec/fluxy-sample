# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vendor'
        db.create_table(u'deals_vendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('web_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('yelp_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('profile_photo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['deals.VendorPhoto'])),
        ))
        db.send_create_signal(u'deals', ['Vendor'])

        # Adding model 'VendorPhoto'
        db.create_table(u'deals_vendorphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.Vendor'])),
        ))
        db.send_create_signal(u'deals', ['VendorPhoto'])

        # Adding model 'Deal'
        db.create_table(u'deals_deal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.Vendor'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_deals', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('instructions', self.gf('django.db.models.fields.CharField')(default='Show to waiter.', max_length=1000)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.VendorPhoto'])),
        ))
        db.send_create_signal(u'deals', ['Deal'])

        # Adding model 'ClaimedDeal'
        db.create_table(u'deals_claimeddeal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fluxy.FluxyUser'])),
            ('deal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.Deal'])),
            ('time_claimed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 20, 0, 0))),
            ('claimed_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('claimed_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('completed_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'deals', ['ClaimedDeal'])


    def backwards(self, orm):
        # Deleting model 'Vendor'
        db.delete_table(u'deals_vendor')

        # Deleting model 'VendorPhoto'
        db.delete_table(u'deals_vendorphoto')

        # Deleting model 'Deal'
        db.delete_table(u'deals_deal')

        # Deleting model 'ClaimedDeal'
        db.delete_table(u'deals_claimeddeal')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deals.claimeddeal': {
            'Meta': {'ordering': "['deal__time_start']", 'object_name': 'ClaimedDeal'},
            'claimed_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'claimed_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'completed_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deals.Deal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_claimed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 20, 0, 0)'}),
            'time_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fluxy.FluxyUser']"})
        },
        u'deals.deal': {
            'Meta': {'ordering': "['time_start']", 'object_name': 'Deal'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'default': "'Show to waiter.'", 'max_length': '1000'}),
            'max_deals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deals.VendorPhoto']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deals.Vendor']"})
        },
        u'deals.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'profile_photo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['deals.VendorPhoto']"}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'yelp_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'deals.vendorphoto': {
            'Meta': {'object_name': 'VendorPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deals.Vendor']"})
        },
        u'fluxy.fluxyuser': {
            'Meta': {'object_name': 'FluxyUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'fb_only': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'vendors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['deals.Vendor']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['deals']