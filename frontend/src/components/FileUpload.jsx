import { useState, useRef } from 'react';
import apiService from '../services/api';

const FileUpload = ({ onUploadSuccess, onUploadError }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);

  // Validate file type - only allow .xlsx and .xls
  const isValidFileType = (fileName) => {
    const extension = fileName.toLowerCase().split('.').pop();
    return extension === 'xlsx' || extension === 'xls';
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const allFiles = Array.from(e.dataTransfer.files);
    const validFiles = allFiles.filter(file => isValidFileType(file.name));
    const invalidFiles = allFiles.filter(file => !isValidFileType(file.name));

    if (invalidFiles.length > 0) {
      const invalidNames = invalidFiles.map(f => f.name).join(', ');
      onUploadError?.(`Invalid file type(s): ${invalidNames}. Only .xlsx and .xls files are allowed.`);
    }

    if (validFiles.length > 0) {
      await handleFileUpload(validFiles);
    } else if (invalidFiles.length > 0) {
      // Only invalid files were dropped
      return;
    }
  };

  const handleFileSelect = async (e) => {
    const allFiles = Array.from(e.target.files);
    
    // Validate file types
    const validFiles = allFiles.filter(file => isValidFileType(file.name));
    const invalidFiles = allFiles.filter(file => !isValidFileType(file.name));

    if (invalidFiles.length > 0) {
      const invalidNames = invalidFiles.map(f => f.name).join(', ');
      onUploadError?.(`Invalid file type(s): ${invalidNames}. Only .xlsx and .xls files are allowed.`);
    }

    if (validFiles.length > 0) {
      await handleFileUpload(validFiles);
    } else if (invalidFiles.length > 0) {
      // Only invalid files were selected - reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      return;
    }
  };

  const handleFileUpload = async (files) => {
    setIsUploading(true);
    setUploadedFiles(files.map(f => f.name));

    try {
      const response = await apiService.uploadFiles(files);
      onUploadSuccess?.(response);
      setUploadedFiles([]);
    } catch (error) {
      onUploadError?.(error.response?.data?.detail || error.message);
      setUploadedFiles([]);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${isDragging ? 'dragging' : ''}`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".xlsx,.xls"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        {isUploading ? (
          <div className="upload-status">
            <div className="spinner"></div>
            <p>Uploading {uploadedFiles.length} file(s)...</p>
            <ul>
              {uploadedFiles.map((name, idx) => (
                <li key={idx}>{name}</li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="upload-prompt">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <p className="upload-text">
              <strong>Click to upload</strong> or drag and drop
            </p>
            <p className="upload-hint">Excel files (.xlsx, .xls) - Multiple files supported</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;

