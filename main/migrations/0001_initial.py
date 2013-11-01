# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Persona'
        db.create_table(u'main_persona', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('cedula', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'main', ['Persona'])

        # Adding model 'TipoServicio'
        db.create_table(u'main_tiposervicio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'main', ['TipoServicio'])

        # Adding model 'Marca'
        db.create_table(u'main_marca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'main', ['Marca'])

        # Adding model 'Servicio'
        db.create_table(u'main_servicio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Persona'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TipoServicio'])),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Marca'])),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(default='En Cola', max_length=12)),
        ))
        db.send_create_signal(u'main', ['Servicio'])


    def backwards(self, orm):
        # Deleting model 'Persona'
        db.delete_table(u'main_persona')

        # Deleting model 'TipoServicio'
        db.delete_table(u'main_tiposervicio')

        # Deleting model 'Marca'
        db.delete_table(u'main_marca')

        # Deleting model 'Servicio'
        db.delete_table(u'main_servicio')


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
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TipoServicio']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'main.tiposervicio': {
            'Meta': {'object_name': 'TipoServicio'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']