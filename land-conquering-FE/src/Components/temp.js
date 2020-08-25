import React, { Component } from 'react'
import axios from 'axios'
import LoadingSpinner from '../Components/LoadingIndicator/LoadingIndicator'
class Temp extends Component {
    constructor(props) {
        super(props)
        this.state = {
            greetingFromServer: '',
            board: null,
            loading: false,
        }
        this.fileInput = React.createRef();
    }
    componentDidMount() {
        axios.get('http://localhost:5000')
            .then(respone => {
                console.log(respone)
                this.setState({
                    greetingFromServer: respone.data
                })
            })
    }
    handleClick = () => {
        this.setState({ loading: true }, () => {
            axios.get('http://localhost:5000/board')
                .then(respone => {
                    console.log(respone.data)
                    this.setState({
                        loading: false,
                        board: respone.data
                    })
                })
        })

    }
    handleSubmit = (event) => {
        event.preventDefault();
        alert(
            `Selected file - ${this.fileInput.current.files[0].name}`
        );
    }
    render() {
        return (
            <div>
                <p>Message from server: {this.state.greetingFromServer}</p>
                <button onClick={this.handleClick}>Get board</button>
                <p>Current board</p>
                <div>{this.state.loading ? <LoadingSpinner /> : this.state.board} </div>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Upload file:
                <input type="file" ref={this.fileInput} />
                    </label>
                    <br />
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    }
}
export default Temp