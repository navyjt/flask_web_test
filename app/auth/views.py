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
from ..tdebug import Tdebug
from ..models import User
from ..sendemail import send_email
from .forms import LoginForm, RegistrationForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
@auth.route('/login',methods=['GET','POST'])
def login():
    td = Tdebug()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            td.pr('开始登录')
            login_user(user,form.remember_me.data)
            td.pr('登录函数执行结束')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


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
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm your accout','auth/email/confirm',user = user,token = token)
        flash('A confirm mail has send to your mailbox')

        if current_app.config['FLASKY_ADMIN']:
            send_email(current_app.config['FLASKY_ADMIN'], '新用户加入','mail/new_user', user=user)
        flash('You can now login.')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))