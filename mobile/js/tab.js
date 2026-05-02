$(function(){

/*현재 URL 경로에서 파일명을 추출하여 해당되는 탭을 block하고 해당 순서의 탭에 tab_on 클래스를 추가*/
var link = window.location.pathname || "";

// URL에서 파일명 추출
var arSplitUrl = link.split("/");    //   "/" 로 전체 url 을 나눈다
var nArLength = arSplitUrl.length;
var arFileName = arSplitUrl[nArLength-1] || "";   // 나누어진 배열의 맨 끝이 파일명이다
var arSplitFileName = arFileName.split(".");   // 파일명을 다시 "." 로 나누면 파일이름과 확장자로 나뉜다
var baseName = arSplitFileName[0] || "";

// 안전한 선택자 이스케이프: jQuery 3.x의 $.escapeSelector를 우선 사용하고, 없으면 폴리필 사용
function escapeSelectorSafe(str) {
	if (!str) return "";
	if ($.escapeSelector) return $.escapeSelector(str);
	return String(str).replace(/([ "!#$%&'()*+,./:;<=>?@[\\\]^`{|}~])/g, "\\$1");
}

// baseName이 비어있으면 선택자 호출을 하지 않도록 안전하게 처리
if (baseName) {
	var esc = escapeSelectorSafe(baseName);

	$('.' + esc).parents('.tabwrap').css('display','block');
	$('.it_' + esc).parents('.intab_wrap').css('display','block');
	console.log(baseName);

	$('.' + esc).parents('div').css('display','block');
	$('.sm_' + esc).parents('div').css('display','block');

	$('.sm_' + esc).addClass('smtab_on');
	$('.' + esc).addClass('it_on');
	$('.' + esc).addClass('tab_on');
}

})