# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
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
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, blank=True)),
        ))
        db.send_create_signal(u'main', ['Persona'])

        # Adding model 'TipoServicio'
        db.create_table(u'main_tiposervicio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'main', ['TipoServicio'])

        # Adding model 'Marca'
        db.create_table(u'main_marca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'main', ['Marca'])

        # Adding model 'Componente'
        db.create_table(u'main_componente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'main', ['Componente'])

        # Adding model 'Servicio'
        db.create_table(u'main_servicio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Persona'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TipoServicio'])),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Marca'])),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('motivo', self.gf('django.db.models.fields.TextField')()),
            ('tecnico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usuarios.Usuario'], null=True, blank=True)),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='empleado_de', null=True, to=orm['usuarios.Usuario'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(default='en-cola', max_length=12, blank=True)),
            ('plazo', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'main', ['Servicio'])

        # Adding M2M table for field componentes on 'Servicio'
        m2m_table_name = db.shorten_name(u'main_servicio_componentes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('servicio', models.ForeignKey(orm[u'main.servicio'], null=False)),
            ('componente', models.ForeignKey(orm[u'main.componente'], null=False))
        ))
        db.create_unique(m2m_table_name, ['servicio_id', 'componente_id'])


    def backwards(self, orm):
        # Deleting model 'Persona'
        db.delete_table(u'main_persona')

        # Deleting model 'TipoServicio'
        db.delete_table(u'main_tiposervicio')

        # Deleting model 'Marca'
        db.delete_table(u'main_marca')

        # Deleting model 'Componente'
        db.delete_table(u'main_componente')

        # Deleting model 'Servicio'
        db.delete_table(u'main_servicio')

        # Removing M2M table for field componentes on 'Servicio'
        db.delete_table(db.shorten_name(u'main_servicio_componentes'))


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
        u'main.componente': {
            'Meta': {'object_name': 'Componente'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'main.marca': {
            'Meta': {'object_name': 'Marca'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'main.persona': {
            'Meta': {'object_name': 'Persona'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'main.servicio': {
            'Meta': {'object_name': 'Servicio'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Persona']"}),
            'componentes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Componente']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'empleado_de'", 'null': 'True', 'to': u"orm['usuarios.Usuario']"}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'en-cola'", 'max_length': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Marca']"}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'motivo': ('django.db.models.fields.TextField', [], {}),
            'plazo': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'tecnico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usuarios.Usuario']", 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TipoServicio']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'main.tiposervicio': {
            'Meta': {'object_name': 'TipoServicio'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'usuarios.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dni': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['main']