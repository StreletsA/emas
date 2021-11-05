import React, { useState, useEffect, Component } from 'react';
import './APIWorker'
import axios from 'axios';
import { Table } from 'react-bootstrap';
import Button from '@restart/ui/esm/Button';
import { ButtonGroup } from 'react-bootstrap';
import * as app from '../App';

var hasChanges = false;

class Student extends Component
{
    constructor(props)
    {
        super(props);

        this.args = props.args;
        this.table = props.table;

        this.personal_number = this.args.PERSONAL_NUMBER;
        this.rank = this.args.RANK;
        this.surname = this.args.SURNAME;
        this.name = this.args.NAME;
        this.patronymic = this.args.PATRONYMIC;
        this.study_group = this.args.STUDY_GROUP;
    }

    render() {
        return(
        
            <tbody>
                <tr>
                    <td>{this.personal_number}</td>
                    <td>{this.rank}</td>
                    <td>{this.surname}</td>
                    <td>{this.name}</td>
                    <td>{this.patronymic}</td>
                    <td>{this.study_group}</td>
                    <td>
                        <ButtonGroup className="me-2" aria-label="First group">
                            <DeleteActionButton personal_number={this.personal_number} table={this.table}/>
                            <UpdateStudentActionButton personal_number={this.personal_number}/>
                        </ButtonGroup>
                    </td>
                </tr>
            </tbody>
        )
    }
}

class DeleteActionButton extends Component
{
    constructor(props)
    {
        super(props);
        this.personal_number = props.personal_number;
        this.table = props.table;
    }

    deleteStudent = () => {
        axios.get(app.host + 'students/delete?personal_number=' + this.personal_number)
        .then(
            (result) => {
                hasChanges = true;
            }
        )
        .then( (res) => console.log(res))
    }

    render()
    {
        return <Button class="btn btn-danger" onClick={() => this.deleteStudent()}>Удалить</Button>
    }
}

class UpdateStudentActionButton extends Component
{
    constructor(props, student)
    {
        super(props);
        this.student = student;
    }

    render()
    {
        return <Button class="btn btn-warning">Изменить</Button>
    }
}

class MainTable extends Component
{
    
    constructor(props, updateButton)
    {
        super(props);
        this.updateButton = updateButton;
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };

        //changesHandler();
    }

    changesHandlerFunc = () => {
        if(hasChanges)
        {
            this.setState({
                error: null,
                isLoaded: false,
                items: []
            });
            this.getStudents();
        }  
    }

    componentDidMount()
    {
        this.getStudents();
        setInterval(this.changesHandlerFunc.bind(this), 1000);
    }

    getStudents = () => {
        axios.get(app.host + 'students/')
        .then(
            (result) => {
                hasChanges = false;
                this.setState({
                    isLoaded: true,
                    items: Object.values(result.data.students).map(function(val) {
                        return <Student args={val} table={this}/>
                    })
                });
            }
        )
    }

    

    padding = (a, b, c, d) => {
        return {
          paddingTop: a,
          paddingRight: b ? b : a,
          paddingBottom: c ? c : a,
          paddingLeft: d ? d : (b ? b : a)
        }
    }

    render()
    {
        const {error, isLoaded, items} = this.state;
        if (error)
            return <p>Error {error.message}</p>
        else if (!isLoaded)
            return <p>Loading...</p>
        else{
            return (
                <div style={this.padding(100,100,100,100)}>
                    <Button class="btn btn-primary" onClick={() => this.getStudents()}>Обновить</Button>
                    <Table striped bordered hover >
                        <thead>
                            <tr>
                                <th>Личный номер</th>
                                <th>Звание</th>
                                <th>Фамилия</th>
                                <th>Имя</th>
                                <th>Отчество</th>
                                <th>Номер учебной группы</th>
                                <th>Действие</th>
                            </tr>
                        </thead>
                        {items}
                    </Table>
                </div>
            )
        }
    }



}
  
  export default MainTable;