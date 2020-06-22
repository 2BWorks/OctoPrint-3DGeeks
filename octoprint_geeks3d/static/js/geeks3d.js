$(function () {
    function Geeks3DViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        $("#geeks3d_test_notificaiton_loading").hide()
        $("#geeks3d_test_notificaiton_sent").hide()


        self.onBeforeBinding = function () {
            self.settings = self.settingsViewModel.settings;
            console.log(self.settings)
        };

        self.onAfterBinding = function () {

        };

        $("#push_print_progress").change(function () {
            if (this.checked) {
                $("#progress_interval").show()
            } else {
                $("#progress_interval").hide()
            }
        });

        $("#geeks3d_regenerate_token").click(function () {
            ok = confirm("Are you sure you want to regenerate your push token? You will have to re-setup your OctoPrint instance from within the app? press OK to continue")
            if (ok) {
                $.ajax({
                    url: API_BASEURL + "plugin/geeks3d",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify({
                        command: "new_token",
                    }),
                    contentType: "application/json; charset=UTF-8"
                }).done(function (data) {
                    $("#settings-geeks3d-token").val(data.token)
                    location.reload();


                });;
            }



        })

        $("#geeks3d_test_notification").click(function () {
                $("#geeks3d_test_notificaiton_loading").show()
                        $("#geeks3d_test_notificaiton_sent").hide()


            $.ajax({
                url: API_BASEURL + "plugin/geeks3d",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "test_notification",
                }),
                contentType: "application/json; charset=UTF-8"
            }).done(function (data) {
                    $("#geeks3d_test_notificaiton_loading").hide()
                            $("#geeks3d_test_notificaiton_sent").show()
            });;

        })
    }


    OCTOPRINT_VIEWMODELS.push({
        construct: Geeks3DViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_printoid, #tab_plugin_printoid, ...
        elements: ["#settings_plugin_geeks3d"]
    });
})
