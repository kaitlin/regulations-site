define("header-view",["jquery","underscore","backbone"],function(e,t,n){var r=n.View.extend({el:".reg-header",initialize:function(){this.$activeEls=e("#menu, #site-header, #reg-content")},events:{"click .toc-toggle":"openTOC"},openTOC:function(e){e.preventDefault(),typeof this.$activeEls!="undefined"&&this.$activeEls.toggleClass("active")}});return r});