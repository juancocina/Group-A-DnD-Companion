$(document).ready(function() {
    // Display Additional Language or Trait Depending on Race Selected
    // $('#id_race').change(function() {
    //     var limit = 0;
    //     var race = $( "#id_race" ).val();

    //     if (race == "Half-Elf") {
    //         $("#default_l").hide();
    //         $("#elf").hide();
    //     }

    //     else if (race == "Human") {
    //         $('.opt_l').prop('disabled', false);
    //         $('.default_l').prop('disabled', true);

    //         $('.opt_t').prop('disabled', true);
    //         $('#id_trait').prop('selectedIndex', 0);
    //     }

    //     else if (race == "Dragonborn") {
    //         $('.opt_t').prop('disabled', false);
    //         $('.opt_t').removeAttr("disabled");
    //         $('.default_t').prop('disabled', true);

    //         $('.opt_l').prop('disabled', true);
    //         $('#id_lang').prop('selectedIndex', 0);
    //     }

    //     else {
    //         $('.opt_l').prop('disabled', true);
    //         $('.opt_t').prop('disabled', true);
    //         $('#id_trait').prop('selectedIndex', 0);
    //         $('#id_lang').prop('selectedIndex', 0);
    //     }
    // });

    // Display Additional Proficiency Depending on Class Selected
    // Number of checked boxes allowed is also displayed
    $('#id_class').change(function() {
        var var_class = $( "#id_class" ).val();
        $('input.chk').prop('checked', false);
        $("input.chk").prop("disabled", true);

        if (var_class == "Barbarian") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl1").prop("disabled", false);
        }

        else if (var_class == "Bard") {
            limit = 3;
            $( "#number" ).html("Select 3");

            $("input.cl2").prop("disabled", false);
        }

        else if (var_class == "Cleric") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl3").prop("disabled", false);
        }

        else if (var_class == "Druid") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl4").prop("disabled", false);
        }

        else if (var_class == "Fighter") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl5").prop("disabled", false);
        }

        else if (var_class == "Monk") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl6").prop("disabled", false);
        }

        else if (var_class == "Paladin") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl7").prop("disabled", false);
        }

        else if (var_class == "Ranger") {
            limit = 3;
            $( "#number" ).html("Select 3");

            $("input.cl8").prop("disabled", false);
        }

        else if (var_class == "Rogue") {
            limit = 4;
            $( "#number" ).html("Select 4");

            $("input.cl9").prop("disabled", false);
        }

        else if (var_class == "Sorcerer") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl10").prop("disabled", false);
        }

        else if (var_class == "Warlock") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl11").prop("disabled", false);
        }

        else if (var_class == "Wizard") {
            limit = 2;
            $( "#number" ).html("Select 2");

            $("input.cl12").prop("disabled", false);
        }

        else {
            limit = 0;
            $( "#number" ).html("Select a Class First");
            $("#most").prop("disabled", true);
        }
    });

    // limit the number of checked boxes
    $('input.chk').on('change', function(evt) {
        if($(this).siblings(':checked').length >= limit) {
            this.checked = false;
        }
     });
  });