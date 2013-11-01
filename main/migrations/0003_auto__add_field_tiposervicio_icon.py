# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TipoServicio.icon'
        db.add_column(u'main_tiposervicio', 'icon',
                      self.gf('django.db.models.fields.CharField')(default='icon', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TipoServicio.icon'
        db.delete_column(u'main_tiposervicio', 'icon')


    models = {
        u'main.marca': {
            'Meta': {'object_name': 'Marca'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'main.persona': {
            'Meta': {'object_name': 'Persona'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'main.servicio': {
            'Meta': {'object_name': 'Servicio'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Persona']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'En Cola'", 'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Marca']"}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TipoServicio']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'main.tiposervicio': {
            'Meta': {'object_name': 'TipoServicio'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']