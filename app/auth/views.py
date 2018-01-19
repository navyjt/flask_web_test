#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-18 16:10:33
# @Author  : laomaizi (navyjt@163.com) All Rights Reserved.
# @Link    : http://45.76.206.38/
# @Version : $Id$

from flask import render_template,redirect,request,url_for,flash,current_app
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .. import db
from ..models import User
from ..sendemail import send_email
from .forms import LoginForm, RegistrationForm

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            print('\n\n====开始登录=======\n\n')
            login_user(user,form.remember_me.data)
            print('\n\n====登录函数执行结束=======\n\n')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid Username or Password')
    return render_template('auth/login.html',form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        if current_app.config['FLASKY_ADMIN']:
            send_email(current_app.config['FLASKY_ADMIN'], '新用户加入','mail/new_user', user=user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)