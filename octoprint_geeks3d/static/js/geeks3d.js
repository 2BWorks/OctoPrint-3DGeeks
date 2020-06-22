$(function() {
    function Geeks3DViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];



          self.onBeforeBinding = function() {
                    self.settings = self.settingsViewModel.settings;
                    console.log(self.settings)
                };

         $("#push_print_progress").change(function() {
                                        if(this.checked){
                                            $("#progress_interval").show()
                                        }else{
                                            $("#progress_interval").hide()
                                        }
                                   });

        $("#geeks3d_regenerate_token").click(function() {
            $.ajax({
            			url: API_BASEURL + "plugin/geeks3d",
            			type: "POST",
            			dataType: "json",
            			data: JSON.stringify({
            				command: "new_token",
            			}),
            			contentType: "application/json; charset=UTF-8"
            			}).done(function(data) {
                            $("#settings-geeks3d-token").val(data.token)
                                  });;

        })

         $("#geeks3d_test_notification").click(function() {
                    $.ajax({
                    			url: API_BASEURL + "plugin/geeks3d",
                    			type: "POST",
                    			dataType: "json",
                    			data: JSON.stringify({
                    				command: "test_notification",
                    			}),
                    			contentType: "application/json; charset=UTF-8"
                    			}).done(function(data) {
                                    alert("Notification has been sent, check your phone")
                                 });;

                })
    }


    OCTOPRINT_VIEWMODELS.push({
            construct: Geeks3DViewModel,
            // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
            dependencies: [ "settingsViewModel" ],
            // Elements to bind to, e.g. #settings_plugin_printoid, #tab_plugin_printoid, ...
            elements: [ "#settings_plugin_geeks3d" ]
        });
})
