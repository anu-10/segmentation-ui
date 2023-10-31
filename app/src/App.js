
import axios from 'axios';
 
import React, { Component } from 'react';

import './App.css';
 
class App extends Component {
 
    state = {
        selectedFile: null,
        img: null,
        fileUploaded: false
    };
    setStateNull = () => {
        this.setState({selectedFile: null, img: null, fileUploaded: false, imgDownload: null});
        this.forceUpdate();
    }
 
    // On file select (from the pop up)
    onFileChange = (event) => {
        
        // Update the state
        this.setState({ selectedFile: event.target.files[0], fileUploaded: false });
        event.target.value = '';
    };
 
    // On file upload (click the upload button)
    onFileUpload = async() => {
        this.setState({ img: null, imgDownload: null});
        if(!this.state.selectedFile)
        {
            alert("No file selected");
            return;
        }
        this.setState({ fileUploaded: false });
        // Create an object of formData
        const formData = new FormData();
        const apiURL = "http://127.0.0.1:5000/image";
        // Update the formData object
        formData.append(
            "file",
            this.state.selectedFile,
            this.state.selectedFile.name
        );
        // Request made to the backend api
        // Send formData object
        axios.post(apiURL, formData, {headers: {
          'Content-Type': 'multipart/form-data',
        },})
      .then((response) => {
        // Handle the response, e.g., display a success message
        console.log(response.data);
        this.setState({ fileUploaded: true });
        alert("File uploaded successfully.");
      })
      .catch((error) => {
        // Handle errors, e.g., display an error message
        alert(error.message);
        console.error(error);
      });
    };
 
    // File content to be displayed after
    // file upload is complete
    fileData = () => {
        
        if (this.state.selectedFile) {
 
            return (
                <div className="grid-item" id = "file-selected">
                    <h2>File Details:</h2>
                    <p>File Name: {this.state.selectedFile.name}</p>
 
                    <p>File Type: {this.state.selectedFile.type}</p>
                    <p>File Size: {Math.round(this.state.selectedFile.size/(1024))} KB</p>
                    <p>
                        Last Modified:{" "}
                        {this.state.selectedFile.lastModifiedDate.toDateString()}
                    </p>
 
                </div>
            );
        } else {
            return (
                <div className="grid-item" id = "file-selected">
                    <br />
                    <h3>No File Selected</h3>
                </div>
            );
        }
    };
    processRequest = async() => {
        
        if(this.state.fileUploaded)
        {
            const apiURL = "http://127.0.0.1:5000/image";
            axios.get(apiURL, {
                responseType: 'blob',
            })
            .then(response => {
                const reader = new FileReader();
                reader.onload = () => {
                    const dataURL = reader.result;
                    this.setState({ img: dataURL, imgDownload: response.data });
                };
                reader.readAsDataURL(response.data);
            })
            .catch(error => {
                console.error('Error downloading the file:', error);
            });
        }
        else
        {
            alert("Upload file first");
        }
        
    }


    handleDownload = () => {
        if(this.state.imgDownload)
        {
            const filename = "image.jpg";
            const url = window.URL.createObjectURL(new Blob([this.state.imgDownload]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
        }
        else
        {
            alert("Click on segment first.");
        }
        
    }
 
    render() {
 
        return (
            <div>
                <h1>Liver Tumor Segmentation</h1>
                
                <div className="grid-container">
                    
                    <div className="grid-item">
                        <h2>Controls</h2>
                        <button className='button-style'>
                            <label htmlFor='file-input'>
                                <input type="file" id="file-input" accept=".nii, .nii.gz" onChange={this.onFileChange} style={{ display: 'none' }}/>
                                Select File
                            </label>
                        </button>
                        <button className='button-style' onClick={this.onFileUpload}>Upload</button>
                        <button className='button-style' onClick={this.processRequest}>Segment</button>
                        <button className='button-style' onClick={this.handleDownload}>Download File</button>
                        <button className='button-style' onClick={this.setStateNull}>Reset</button>
                    </div>
                    {this.fileData()}
                
                    
                    {this.state.img && (
                        <div className="grid-item output">
                            <h2>Output Mask</h2>
                            <img src={this.state.img} alt="" />
                        </div>
                    )}
                
                </div>

                
            </div>
        );
    }
}
 
export default App;