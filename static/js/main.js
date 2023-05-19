jQuery(document).ready(function($)
{
	"use strict";

  var sid = $('#sid').attr('content')
  var page = $('#page').attr('content')
  var detail = $('#detail').attr('content')
  var description = $('#descriptionn').attr('content')
  var information = $('#information').attr('content')
  var url = $('#url').attr('content')
  var hostname = location.href.split('/')[0]+'//'+location.hostname
  if (location.port != '') { hostname = hostname+':'+location.port }
  var urlpath = location.pathname.split('/')
  if (urlpath[1] != '') {
    if (location.pathname != url) { location.href = url }
    if (urlpath[1] != page) { location.href = '/'+page }
  }

  if (page == 'cadastro') {
    $('#send').click(function () {
      send_form('#form', {'method':['add', 'user']}, '/perfil',[])
    })
  } else if (page == 'entrar') {
    $('#send').click(function () {
      send_form('#form', {'method':['add', 'login']}, '/perfil',[])
    })
  }

  $('.btnTest').click(function () {
    send_form('#form', {'method':['add', 'teste']}, 'Enviado!', [''])
  })

  $('.showModal').click(function () {
    $('#'+$(this).attr('modal')).removeClass('d-none')
  })
  $('.closeModal').click(function () {
    $('#'+$(this).attr('modal')).addClass('d-none')
  })
  $('.monetary').keyup(function (e) {
    var number = ['0','1','2','3','4','5','6','7','8','9','.']
    var view = $(this)
    var content = $('#'+view.attr('content'))
    var value = content.val()
    var key = e.key.toString()
    if (number.indexOf(key) > -1) {
      if (value == '') { value = '0,0'+key }
      else if (value.length == 4) {
        if (value.substring(0,1) == '0') { value = value.substring(2,3)+','+value.substring(3,4)+key }
        else { value = value.substring(0,1)+value.substring(2,3)+','+value.substring(3,4)+key }
      } else if (value.length == 5) {
        value = value.substring(0,2)+value.substring(3,4)+','+value.substring(4,5)+key
      }
    } else if (key == 'Backspace') { // 40.00
      if (value.length == 4) { value = '0,'+value.substring(0,1)+value.substring(2,3) }
      else if (value.length == 5) { value = value.substring(0,1)+','+value.substring(1,2)+value.substring(3,4) }
      else { value = value.substring(0,2)+','+value.substring(2,3)+value.substring(4,5) }
    }
    content.val(value)
    view.val('R$'+value)
  })
  $('.btnLink').click(function () {
    $(location).attr('href', $(this).attr('href'))
  })
  $('.toCopy').click(function () {
    var text = $('#'+$(this).attr('content')).html()
    $('#'+$(this).attr('content')+'-icon-init').addClass('d-none')
    $('#'+$(this).attr('content')+'-icon-copied').removeClass('d-none')
    navigator.clipboard.writeText(text);
    setTimeout(() => {
      $('#'+$(this).attr('content')+'-icon-copied').addClass('d-none')
      $('#'+$(this).attr('content')+'-icon-init').removeClass('d-none')
    }, 1000);
  })
  $('.toWait').click(function () {
    var text = $(this).html()
    $(this).addClass('disabled')
    $(this).attr('disabled', 'disabled')
    if (text != '') { $(this).html('Aguarde') }
    setTimeout(() => {
      $(this).removeClass('disabled')
      $(this).removeAttr('disabled')
      if (text != '') { $(this).html(text) }
    }, 2500)
  })
  $(document.body).on('click', '.failure', function () {
    $(this).removeClass('failure')
  })

  $('.searchSelect').change(function () { 
    $('.searchInput').each(function () { $(this).val('') })
    toSearch($(this).val().toLowerCase(), $(this).attr('target')) 
  })
  $('.searchInput').keyup(function () { 
    $('.searchSelect').each(function () { $(this).val('*') })
    toSearch($(this).val().toLowerCase(), $(this).attr('target'))
  })
  function toSearch(text, target) {
    var results = 0
    $('.'+target).each(function() {
      if (text != '*' && text != '') {
        if ($(this).attr('searchStatus').toLowerCase().includes(text)) { 
          $(this).removeClass('d-none')
          results += 1
        } else { $(this).addClass('d-none') }
      } else { $(this).removeClass('d-none') }
    })
    if (results == 0) {
      if (text == '*' || text == '') { $('#searchMsg-'+target).html('Mostrando todos os itens') }
      else { $('#searchMsg-'+target).html('Nenhum resultado correspondente') }
    } else { $('#searchMsg-'+target).html('Mostrando '+results+' resultado(s)') }
  }

  function send(data, action='', form='') {
    var data = data
    data['sid'] = sid
    $.ajax({
      type: "POST", 
      url: "/listener",
      data : JSON.stringify(data),
      contentType: "application/json",
      success: function(response){
        var response = jQuery.parseJSON(response);
        if (response.success) {
          if (action == 'reload') { location.reload(true) } 
          else if (action.indexOf('/') != -1) { $(location).prop('href', action) } 
          else { form_alert(form, true, action) }
        } else { form_alert(form, false, response.description) }
      },
      error: function() { alert('Erro interno! Por Favor, Tente novamente mais tarde!') }
    })
  }		

  function send_form(form, preset={}, action='', allowEmpty=[]) {
    if (has_empty(form, allowEmpty)) {
      form_alert(form, false, 'Preencha todas as informações obrigatórias(*) para prosseguir')
      return
    }
    var data = get(form, preset)
    data['sid'] = sid
    $.ajax({
      type: "POST",
      url: "/listener",
      data : JSON.stringify(data),
      contentType: "application/json",
      success: function(response){
        var response = jQuery.parseJSON(response);
        if (response.success) {
          if (action == 'reload') { location.reload(true) }
          else if (action.indexOf('/') != -1) { $(location).prop('href', action) }
          else { form_alert(form, true, action) }
        } else { form_alert(form, false, response.description) }
      },
      error: function() { form_alert(form, false, 'Erro interno! Por Favor, Tente novamente mais tarde!') }
    })
  }	

  function form_alert(form, success=null, msg='Teste realizado com sucesso!', timer=2500) {
    var am = $('<div class="am"><div class="am-text"></div></div>')
    $(form).append(am)
    setTimeout(() => {
      am.addClass('active')
      if (success == true) { am.children('.am-text').addClass('bg-success') }
      else if (success == false) { am.children('.am-text').addClass('bg-danger') }
      am.children('.am-text').html(msg)
      setTimeout(() => { 
        am.removeClass('active') 
        setTimeout(() => {
          am.remove() 
        }, 200)
      }, timer);
    }, 200)
  }
  
  function get(form, data={}) {
    var elements = ['input', 'select', 'textarea']
    $(elements).each(function (i, kid) {
      $(form).find($(kid)).each(function () {
        if ($(this).attr('id')) {
          if ($(this).attr('id').indexOf('-') != -1) { var id = $(this).attr('id').split('-')[0] } 
          else { var id = $(this).attr('id') }
          if ($(this).attr('type') == 'checkbox') { data[id] = $(this).is(":checked") }
          else { data[id] = $(this).val() }
        }
      })
    })
    return(data)
  }

  function has_empty(form, optional=[]) {
    var empty = false
    var elements = ['input', 'select']
    $(elements).each(function (i, kid) {
      $(form).find($(kid)).each(function () {
        if ($(this).attr('id')) {
          if ($.inArray($(this).attr('id').split('-')[0], optional) == -1) {
            if ($(this).val() == '') { empty = true; $(this).addClass('failure') }
          }
        }
      })
    })
    return(empty)
  }

  $('#year').html(new Date().getFullYear())

  setTimeout(() => {
    $('.loader').removeClass('active')
  }, 200)

});