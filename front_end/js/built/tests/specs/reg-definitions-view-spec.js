define(["underscore","backbone","jquery","definition-view","regs-data","samplejson"],function(e,t,n,r,i,s){describe("Definitions views",function(){i.parse(s),n("body").append('<div id="2345-6-a">sdfsd</div>').append('<a id="2345-4">sdfds</a>');var e=new r({id:"2345-6-a",$anchor:n("#2345-4")});it("should have the view instance",function(){expect(e).toBeTruthy()}),it("should store the definition content",function(){expect(e.model.content).toEqual("this is where we'd load the api response for 2345-6-a in json format.")}),it("should store the parent link",function(){expect(e.model.$anchor).toEqual(n("#2345-4"))}),it("should tell the state obj that its open",function(){})})});