<template>
  <div class="document-upload-page">
    <!-- Sidebar for uploaded documents -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>已上传文档</h3>
        <span class="document-count">{{ documents.length }} 个文档</span>
      </div>

      <div class="sidebar-content">
        <!-- Loading state -->
        <div v-if="documentsLoading" class="loading-state">
          <el-icon class="is-loading"><Loading /></el-icon>
          <p>加载中...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="documents.length === 0" class="empty-state">
          <div class="empty-content">
            <h4>暂无文档</h4>
            <p>请在右侧上传您的文档</p>
          </div>
        </div>

        <!-- Documents list -->
        <div v-else class="documents-list">
          <div
            v-for="document in documents"
            :key="document.id"
            class="document-item"
            :class="{ selected: selectedDocument && selectedDocument.id === document.id }"
            @click="selectDocument(document)"
          >
            <div class="document-icon">
              <el-icon v-if="document.is_local_file"><Document /></el-icon>
              <el-icon v-else><EditPen /></el-icon>
            </div>
            <div class="document-info">
              <h4 class="document-name">{{ document.filename }}</h4>
              <p class="document-meta">
                <span class="collection-tag">{{ getCollectionDisplayName(document.collection_type) }}</span>
                <span class="upload-method">{{ document.upload_method === 'file' ? '文件' : '文本' }}</span>
              </p>
              <p class="document-date">{{ formatDate(document.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main content area -->
    <main class="main-content">
      <div class="content-area">
        <div class="upload-section">
          <div class="section-header">
            <h2>文档上传</h2>
            <p>上传您的简历、项目经验等文档，或直接输入文本内容</p>
          </div>

          <!-- Upload methods -->
          <div class="upload-methods">
            <!-- File upload -->
            <div class="upload-method file-upload">
              <div class="method-header">
                <el-icon class="method-icon"><FolderOpened /></el-icon>
                <h3>上传本地文件</h3>
              </div>
              <div class="method-content">
                <el-upload
                  ref="fileUpload"
                  class="upload-dragger"
                  drag
                  :auto-upload="false"
                  :on-change="handleFileSelect"
                  :file-list="fileList"
                  :limit="1"
                  accept=".txt,.md,.pdf,.doc,.docx"
                >
                  <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
                  <div class="el-upload__text">
                    将文件拖到此处，或<em>点击上传</em>
                  </div>
                  <template #tip>
                    <div class="el-upload__tip">
                      支持 txt, md, pdf, doc, docx 格式文件
                    </div>
                  </template>
                </el-upload>

                <!-- Collection selection for file upload -->
                <div class="upload-options">
                  <div class="option-group">
                    <label>文档分类：</label>
                    <el-select
                      v-model="fileUploadOptions.collection_type"
                      placeholder="自动分类"
                      clearable
                      size="default"
                    >
                      <el-option label="自动分类（推荐）" :value="null" />
                      <el-option
                        v-for="collection in availableCollections"
                        :key="collection.key"
                        :label="collection.label"
                        :value="collection.key"
                      />
                    </el-select>
                  </div>
                </div>

                <el-button
                  type="primary"
                  size="large"
                  @click="uploadFile"
                  :loading="fileUploading"
                  :disabled="!selectedFile"
                  class="upload-btn"
                >
                  {{ fileUploading ? '上传中...' : '上传文件' }}
                </el-button>
              </div>
            </div>

            <!-- Text input -->
            <div class="upload-method text-upload">
              <div class="method-header">
                <el-icon class="method-icon"><Edit /></el-icon>
                <h3>直接输入文本</h3>
              </div>
              <div class="method-content">
                <el-input
                  v-model="textContent"
                  type="textarea"
                  placeholder="请输入文档内容，如简历信息、项目经验等..."
                  :rows="12"
                  maxlength="10000"
                  show-word-limit
                  class="text-input"
                  :autosize="{ minRows: 12, maxRows: 20 }"
                />

                <!-- Options for text upload -->
                <div class="upload-options">
                  <div class="option-group">
                    <label>文档标题：</label>
                    <el-input
                      v-model="textUploadOptions.filename"
                      placeholder="自动生成（推荐）"
                      clearable
                      size="default"
                    />
                  </div>
                  <div class="option-group">
                    <label>文档分类：</label>
                    <el-select
                      v-model="textUploadOptions.collection_type"
                      placeholder="自动分类"
                      clearable
                      size="default"
                    >
                      <el-option label="自动分类（推荐）" :value="null" />
                      <el-option
                        v-for="collection in availableCollections"
                        :key="collection.key"
                        :label="collection.label"
                        :value="collection.key"
                      />
                    </el-select>
                  </div>
                </div>

                <el-button
                  type="primary"
                  size="large"
                  @click="uploadText"
                  :loading="textUploading"
                  :disabled="!textContent.trim()"
                  class="upload-btn"
                >
                  {{ textUploading ? '上传中...' : '上传文本' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import {
  Document,
  EditPen,
  FolderOpened,
  UploadFilled,
  Edit,
  Loading
} from '@element-plus/icons-vue'
import { documentService } from '@/services/api'

export default {
  name: 'Documents',
  components: {
    Document,
    EditPen,
    FolderOpened,
    UploadFilled,
    Edit,
    Loading
  },
  data() {
    return {
      // Documents list
      documents: [],
      documentsLoading: false,
      selectedDocument: null,

      // File upload
      selectedFile: null,
      fileList: [],
      fileUploading: false,
      fileUploadOptions: {
        collection_type: null
      },

      // Text upload
      textContent: '',
      textUploading: false,
      textUploadOptions: {
        filename: '',
        collection_type: null
      },

      // Collections
      availableCollections: [
        { key: 'resumes', label: '个人简历' },
        { key: 'projects_experience', label: '项目经验' },
        { key: 'job_postings', label: '职位信息' },
        { key: 'interviews', label: '面试记录' },
        { key: 'interview_qna_bank', label: '面试题库' },
        { key: 'code_analysis', label: '代码分析' },
        { key: 'industry_trends', label: '行业趋势' }
      ]
    }
  },

  async mounted() {
    console.log('Documents component mounted')
    await this.loadDocuments()
  },

  methods: {
    async loadDocuments() {
      this.documentsLoading = true
      try {
        const response = await documentService.getDocumentList()
        this.documents = response.data.documents || []
        console.log('Loaded documents:', this.documents)
      } catch (error) {
        console.error('Failed to load documents:', error)
        this.$message.error('加载文档列表失败，请稍后重试')
      } finally {
        this.documentsLoading = false
      }
    },

    selectDocument(document) {
      this.selectedDocument = document
      console.log('Selected document:', document)
    },

    handleFileSelect(file) {
      this.selectedFile = file.raw
      this.fileList = [file]
      console.log('File selected:', file)
    },

    async uploadFile() {
      if (!this.selectedFile) {
        this.$message.warning('请先选择文件')
        return
      }

      this.fileUploading = true
      try {
        // Read file content
        const fileContent = await this.readFileAsText(this.selectedFile)

        const uploadData = {
          content: fileContent,
          filename: this.selectedFile.name,
          collection_type: this.fileUploadOptions.collection_type
        }

        const response = await documentService.ingestDocument(uploadData)

        this.$message.success('文件上传成功！')
        console.log('File upload response:', response.data)

        // Reset form
        this.selectedFile = null
        this.fileList = []
        this.fileUploadOptions.collection_type = null
        this.$refs.fileUpload.clearFiles()

        // Reload documents list
        await this.loadDocuments()

      } catch (error) {
        console.error('File upload failed:', error)
        this.$message.error('文件上传失败：' + (error.response?.data?.detail || error.message))
      } finally {
        this.fileUploading = false
      }
    },

    async uploadText() {
      if (!this.textContent.trim()) {
        this.$message.warning('请输入文本内容')
        return
      }

      this.textUploading = true
      try {
        const uploadData = {
          content: this.textContent.trim(),
          filename: this.textUploadOptions.filename || null,
          collection_type: this.textUploadOptions.collection_type
        }

        const response = await documentService.ingestDocument(uploadData)

        this.$message.success('文本上传成功！')
        console.log('Text upload response:', response.data)

        // Reset form
        this.textContent = ''
        this.textUploadOptions.filename = ''
        this.textUploadOptions.collection_type = null

        // Reload documents list
        await this.loadDocuments()

      } catch (error) {
        console.error('Text upload failed:', error)
        this.$message.error('文本上传失败：' + (error.response?.data?.detail || error.message))
      } finally {
        this.textUploading = false
      }
    },

    readFileAsText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = (e) => reject(e)
        reader.readAsText(file, 'UTF-8')
      })
    },

    getCollectionDisplayName(collectionType) {
      const collection = this.availableCollections.find(c => c.key === collectionType)
      return collection ? collection.label : collectionType
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.document-upload-page {
  min-height: 100vh;
  display: flex;
  background: #f5f5f5;
  position: relative;
}

/* Sidebar styles */
.sidebar {
  width: 320px;
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
}

.document-count {
  color: #666;
  font-size: 14px;
  background: #f0f2f5;
  padding: 4px 8px;
  border-radius: 12px;
}

.sidebar-content {
  padding: 16px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #606266;
}

.loading-state .el-icon {
  font-size: 24px;
  margin-bottom: 12px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.empty-content {
  text-align: center;
  color: #606266;
}

.empty-content h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.empty-content p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

/* Documents list */
.documents-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.document-item {
  display: flex;
  align-items: flex-start;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.document-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.document-item.selected {
  border-color: #409eff;
  background: #f0f8ff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.document-icon {
  margin-right: 12px;
  color: #409eff;
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.document-info {
  flex: 1;
  min-width: 0;
}

.document-name {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  word-break: break-word;
}

.document-meta {
  margin: 0 0 4px 0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.collection-tag {
  background: #e1f3d8;
  color: #67c23a;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.upload-method {
  background: #f0f2f5;
  color: #606266;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.document-date {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

/* Main content styles */
.main-content {
  flex: 1;
  margin-left: 50px;
  padding: 40px;
  height: 90vh;
  overflow-y: auto;
}

.content-area {
  width: 90%;
  height: 90%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.upload-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.section-header {
  padding: 24px 32px;
  border-bottom: 1px solid #ebeef5;
  background: #fafbfc;
}

.section-header h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.section-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

/* Upload methods */
.upload-methods {
  padding: 32px;
  display: grid;
  grid-template-columns: 1fr 2fr;  /* 文件上传:文本输入 = 1:2 */
  gap: 32px;
  flex: 1;
  overflow: hidden;
}

.upload-method {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.method-header {
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  gap: 12px;
}

.method-icon {
  font-size: 24px;
  color: #409eff;
}

.method-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.method-content {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* File upload specific styles */
.upload-dragger {
  width: 100%;
}

.upload-dragger .el-upload {
  width: 100%;
}

.upload-dragger .el-upload-dragger {
  width: 100%;
  height: 160px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.upload-dragger .el-upload-dragger:hover {
  border-color: #409eff;
  background: #f0f8ff;
}

.upload-dragger .el-icon--upload {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-dragger .el-upload__text {
  color: #606266;
  font-size: 14px;
}

.upload-dragger .el-upload__text em {
  color: #409eff;
  font-style: normal;
}

/* Text input styles */
.text-input {
  margin-bottom: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.text-input .el-textarea {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.text-input .el-textarea__inner {
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  line-height: 1.6;
  flex: 1;
  min-height: 300px;
  resize: vertical;
}

.text-input .el-textarea__inner:focus {
  border-color: #409eff;
}

/* Upload options */
.upload-options {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.option-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-group label {
  min-width: 80px;
  color: #606266;
  font-size: 14px;
  font-weight: 500;
}

.option-group .el-select,
.option-group .el-input {
  flex: 1;
}

/* Upload button */
.upload-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: 8px;
  margin-top: 8px;
}

/* Responsive design */
@media (max-width: 1200px) {
  .upload-methods {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .content-area {
    width: 95%;
    height: 95%;
  }
}

@media (max-width: 768px) {
  .document-upload-page {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
    max-height: 800px;
  }

  .main-content {
    margin-left: 0;
    padding: 20px;
    height: calc(100vh - 300px);
  }

  .content-area {
    width: 100%;
    height: 100%;
  }

  .upload-methods {
    padding: 20px;
    grid-template-columns: 1fr;
  }

  .section-header {
    padding: 20px;
  }

  .text-input .el-textarea__inner {
    min-height: 150px;
  }
}
</style>