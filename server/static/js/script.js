const api_address = "/emas/api/"
var request = new XMLHttpRequest();
var list_for_deleting = []

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" btn btn-light", "btn btn-secondary");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " btn btn-light";

    if (tabName == "all_persons"){
         get_all_persons();
    }
}

function get_all_persons(){



    request.open('GET', api_address + "students/");

    // Здесь мы получаем ответ от сервера на запрос, лучше сказать ждем ответ от сервера
    request.addEventListener("readystatechange", get_all_persons_event_listener);

    // Выполняем запрос
    request.send();

}

function delete_person(evt){

    request.open('GET', api_address + "students/delete?personal_number=" + evt.target.id);

    request.addEventListener("readystatechange", get_all_persons_after_deleting);

    // Выполняем запрос
    request.send();
}

function delete_many_persons(event){
    request.open('GET', api_address + "students/delete?personal_number=" + list_for_deleting[0]);
    request.addEventListener("readystatechange", delete_many_persons_listener);
    request.send();
}

function delete_many_persons_listener(event){
    if (request.readyState === 4 && request.status === 200){
            list_for_deleting = list_for_deleting.filter(item => item !== list_for_deleting[0]);
            request.removeEventListener("readystatechange", delete_many_persons_listener);
            if (list_for_deleting.length > 0){
                request.open('GET', api_address + "persons/delete?personal_number=" + list_for_deleting[0]);
                request.addEventListener("readystatechange", delete_many_persons_listener);
                request.send();
            }
            else{
                get_all_persons();
            }

    }
}

function get_all_persons_after_deleting(evt){
    if (request.readyState === 4 && request.status === 200){
            get_all_persons();
            request.removeEventListener("readystatechange", get_all_persons_after_deleting);
    }
}

function search_persons(event){

    var personal_number = document.getElementById("pers_num_opt").value;
    var rank = document.getElementById("rank_opt").value;
    var study_group = document.getElementById("study_group_opt").value;
    var surname = document.getElementById("surname_opt").value;
    var name = document.getElementById("name_opt").value;
    var patronymic = document.getElementById("patronymic_opt").value;

    req = "?personal_number=" + personal_number +
            "&rank=" + rank +
            "&study_group=" + study_group +
            "&surname=" + surname +
            "&name=" + name +
            "&patronymic=" + patronymic;

    request.open('GET', api_address + "students/search" + req);
    request.addEventListener("readystatechange", search_persons_listener);
    request.send();
}

function search_persons_listener(event){
    if (request.readyState === 4 && request.status === 200){
        var json = request.responseText;
        var persons = JSON.parse(json).persons;

        var all_persons_table = document.getElementById("all_persons_table");

        while (all_persons_table.getElementsByTagName('tr').length > 1)
            {
                all_persons_table.deleteRow(all_persons_table.getElementsByTagName('tr').length - 1);
            }

        if (typeof persons != "undefined"){
                for (var i = 0; i < persons.length; i++) {

	            var tr = document.createElement('tr');

                var td_check = document.createElement('input');
                td_check.type = 'checkbox';
                td_check.id = persons[i].personal_number;
                var td_personal_number = document.createElement('td');
                var td_rank = document.createElement('td');
                var td_surname = document.createElement('td');
                var td_name = document.createElement('td');
                var td_patronymic = document.createElement('td');
                var td_study_group = document.createElement('td');
                var div_control = document.createElement('div');

                div_control.className = "control_panel";

                td_check.addEventListener('change', (evt) => {

                  if (evt.target.checked) {
                    list_for_deleting.push(evt.target.id);
                  } else {
                    list_for_deleting = list_for_deleting.filter(item => item !== evt.target.id);
                  }

                });

                var update_person_button = document.createElement('button');
                update_person_button.className = 'btn btn-warning';
                update_person_button.appendChild(document.createTextNode("Подробнее/Изменить"));
                var delete_person_button = document.createElement('button');
                delete_person_button.className = 'btn btn-danger';
                delete_person_button.appendChild(document.createTextNode("Удалить"));
                delete_person_button.id = persons[i].personal_number;
                delete_person_button.addEventListener("click", delete_person);

                td_personal_number.appendChild(document.createTextNode(persons[i].personal_number));
                td_rank.appendChild(document.createTextNode(persons[i].rank));
                td_surname.appendChild(document.createTextNode(persons[i].surname));
                td_name.appendChild(document.createTextNode(persons[i].name));
                td_patronymic.appendChild(document.createTextNode(persons[i].patronymic));
                td_study_group.appendChild(document.createTextNode(persons[i].study_group));

                div_control.appendChild(update_person_button);
                div_control.appendChild(delete_person_button);

                tr.appendChild(td_check);
                tr.appendChild(td_personal_number);
                tr.appendChild(td_rank);
                tr.appendChild(td_surname);
                tr.appendChild(td_name);
                tr.appendChild(td_patronymic);
                tr.appendChild(td_study_group);
                tr.appendChild(div_control);

	            all_persons_table.appendChild(tr);
            }

        }



        request.removeEventListener("readystatechange", search_persons_listener);
    }
}

function get_all_persons_event_listener(event)
{
    var all_persons_table = document.getElementById("all_persons_table");
    if (request.readyState === 4 && request.status === 200) {

            while (all_persons_table.getElementsByTagName('tr').length > 1)
            {
                all_persons_table.deleteRow(all_persons_table.getElementsByTagName('tr').length - 1);
            }

            var json = request.responseText;
            var persons = JSON.parse(json).students;

            //alert(persons[0].name);

            if (typeof persons != "undefined"){
                for (var i = 0; i < persons.length; i++) {

	            var tr = document.createElement('tr');

                var td_check = document.createElement('input');
                td_check.type = 'checkbox';
                td_check.id = persons[i].personal_number;
                var td_personal_number = document.createElement('td');
                var td_rank = document.createElement('td');
                var td_surname = document.createElement('td');
                var td_name = document.createElement('td');
                var td_patronymic = document.createElement('td');
                var td_study_group = document.createElement('td');
                var div_control = document.createElement('div');

                div_control.className = "control_panel";

                td_check.addEventListener('change', (evt) => {

                  if (evt.target.checked) {
                    list_for_deleting.push(evt.target.id);
                  } else {
                    list_for_deleting = list_for_deleting.filter(item => item !== evt.target.id);
                  }

                });

                var update_person_button = document.createElement('button');
                update_person_button.className = 'btn btn-warning';
                update_person_button.appendChild(document.createTextNode("Подробнее/Изменить"));
                var delete_person_button = document.createElement('button');
                delete_person_button.className = 'btn btn-danger';
                delete_person_button.appendChild(document.createTextNode("Удалить"));
                delete_person_button.id = persons[i].personal_number;
                delete_person_button.addEventListener("click", delete_person);

                td_personal_number.appendChild(document.createTextNode(persons[i].PERSONAL_NUMBER));
                td_rank.appendChild(document.createTextNode(persons[i].RANK));
                td_surname.appendChild(document.createTextNode(persons[i].SURNAME));
                td_name.appendChild(document.createTextNode(persons[i].NAME));
                td_patronymic.appendChild(document.createTextNode(persons[i].PATRONYMIC));
                td_study_group.appendChild(document.createTextNode(persons[i].STUDY_GROUP));

                div_control.appendChild(update_person_button);
                div_control.appendChild(delete_person_button);

                tr.appendChild(td_check);
                tr.appendChild(td_personal_number);
                tr.appendChild(td_rank);
                tr.appendChild(td_surname);
                tr.appendChild(td_name);
                tr.appendChild(td_patronymic);
                tr.appendChild(td_study_group);
                tr.appendChild(div_control);

	            all_persons_table.appendChild(tr);
            }

        }

        }

}