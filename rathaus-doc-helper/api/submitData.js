const multipart = require('parse-multipart');
const { BlobServiceClient } = require('@azure/storage-blob');

module.exports = async function (context, req) {
    try {
        // Check if we have the required data
        if (!req.body || !req.headers['content-type']) {
            return {
                status: 400,
                body: { message: 'Please provide the required form data' }
            };
        }

        // Parse the multipart form data
        const bodyBuffer = Buffer.from(req.body);
        const boundary = multipart.getBoundary(req.headers['content-type']);
        const parts = multipart.Parse(bodyBuffer, boundary);

        // Get form data
        const formData = JSON.parse(parts.find(part => part.name === 'formData').data);
        const files = parts.filter(part => part.name === 'files');

        // Connect to Azure Blob Storage
        const blobServiceClient = BlobServiceClient.fromConnectionString(process.env.AzureWebJobsStorage);
        const containerClient = blobServiceClient.getContainerClient('documents');

        // Upload files to blob storage
        const uploadedFiles = [];
        for (const file of files) {
            const blobName = `${Date.now()}-${file.filename}`;
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);
            await blockBlobClient.upload(file.data, file.data.length);
            uploadedFiles.push(blobName);
        }

        const submission = {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            isRegistered: formData.isRegistered,
            isEU: formData.isEU,
            selectedService: formData.selectedService,
            files: uploadedFiles
        };

        return {
            status: 200,
            body: {
                message: 'Documents uploaded successfully',
                submissionId: submission.id
            }
        };
    } catch (error) {
        console.error('Error processing submission:', error);
        return {
            status: 500,
            body: {
                message: 'Error processing the submission',
                error: error.message
            }
        };
    }
};
