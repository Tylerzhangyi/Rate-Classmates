import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'
import client from '../api/client'

export const useDataStore = defineStore('data', () => {
  const schools = ref([])
  const students = ref([])
  const badges = ref([])
  const studentBadges = ref([])
  const ratingsByStudent = reactive({})
  const ratingsByRater = reactive({})
  const schoolApplications = ref([])
  const studentApplications = ref([])
  const loading = ref(false)
  const loaded = ref(false)
  const error = ref('')

  async function loadInitial() {
    if (loaded.value) return
    loading.value = true
    error.value = ''
    try {
      await Promise.all([fetchSchools(), fetchStudents(), fetchBadges()])
      loaded.value = true
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function fetchSchools() {
    const res = await client.get('schools')
    schools.value = (res.data.data || []).map(s => ({
      id: s.school_id,
      school_name: s.school_name,
      created_at: s.created_at
    }))
  }

  async function fetchStudents(params = {}) {
    const res = await client.get('students', { params })
    students.value = (res.data.data || []).map(s => ({
      id: s.student_id,
      school_id: s.school_id,
      school_name: s.school_name,
      name: s.name,
      grade: s.grade,
      avg_score: s.avg_score,
      rating_count: s.rating_count,
      dominant_rating: s.avg_score ? Math.round(s.avg_score) : 0
    }))
  }

  async function fetchStudentById(studentId) {
    const res = await client.get(`students/${studentId}`)
    const s = res.data.data
    const mapped = {
      id: s.student_id,
      school_id: s.school_id,
      school_name: s.school_name,
      name: s.name,
      grade: s.grade,
      avg_score: s.avg_score,
      rating_count: s.rating_count,
      dominant_rating: s.avg_score ? Math.round(s.avg_score) : 0
    }
    const idx = students.value.findIndex(item => item.id === mapped.id)
    if (idx >= 0) students.value[idx] = mapped
    else students.value.push(mapped)
    return mapped
  }

  async function fetchBadges() {
    const res = await client.get('badges')
    badges.value = (res.data.data || []).map(b => ({
      id: b.badge_id,
      ...b
    }))
  }

  async function fetchStudentBadges(studentId) {
    const res = await client.get(`student-badges/${studentId}`)
    studentBadges.value = studentBadges.value
      .filter(b => b.student_id !== studentId)
      .concat(
        (res.data.data || []).map(b => ({
          ...b,
          student_id: studentId
        }))
      )
  }

  async function fetchStudentRatings(studentId) {
    const res = await client.get(`students/${studentId}/ratings`)
    ratingsByStudent[studentId] = (res.data.data || []).map(r => ({
      id: r.rating_id,
      rater_id: r.rater_id,
      rater_name: r.rater_name,
      target_id: r.target_id,
      score: r.score,
      comment: r.comment,
      created_at: r.created_at
    }))
    return ratingsByStudent[studentId]
  }

  function getStudentRatings(studentId) {
    return ratingsByStudent[studentId] || []
  }

  async function submitRating(rating) {
    // rater_id 从 session 获取，不需要传递
    const res = await client.post('ratings', {
      target_id: rating.target_id,
      score: rating.score,
      comment: rating.comment || ''
    })
    await Promise.all([fetchStudentRatings(rating.target_id), fetchStudentById(rating.target_id)])
    return res.data.data
  }

  async function fetchMyRatings(raterId) {
    const res = await client.get('ratings', { params: { rater_id: raterId } })
    ratingsByRater[raterId] = (res.data.data || []).map(r => ({
      id: r.rating_id,
      target_id: r.target_id,
      target_name: r.target_name,
      score: r.score,
      comment: r.comment,
      created_at: r.created_at
    }))
    return ratingsByRater[raterId]
  }

  function getMyRatings(raterId) {
    return ratingsByRater[raterId] || []
  }

  async function createSchoolApplication(application) {
    const res = await client.post('school-applications', application)
    return res.data.data
  }

  async function createStudentApplication(application) {
    const res = await client.post('student-applications', application)
    return res.data.data
  }

  async function fetchSchoolApplications(params = {}) {
    const res = await client.get('school-applications', { params })
    schoolApplications.value = (res.data.data || []).map(a => ({
      id: a.application_id,
      applicant_id: a.applicant_id,
      school_name: a.school_name,
      contact: a.contact,
      reason: a.reason,
      status: a.status,
      created_at: a.created_at,
      updated_at: a.updated_at
    }))
  }

  async function fetchStudentApplications(params = {}) {
    const res = await client.get('student-applications', { params })
    studentApplications.value = (res.data.data || []).map(a => ({
      id: a.application_id,
      applicant_id: a.applicant_id,
      student_name: a.student_name,
      school_id: a.school_id,
      school_name: a.school_name,
      grade: a.grade,
      reason: a.reason,
      status: a.status,
      created_at: a.created_at,
      updated_at: a.updated_at
    }))
  }

  function getSchoolApplications(status = null) {
    if (!status) return schoolApplications.value
    return schoolApplications.value.filter(app => app.status === status)
  }

  function getStudentApplications(status = null) {
    if (!status) return studentApplications.value
    return studentApplications.value.filter(app => app.status === status)
  }

  async function updateSchoolApplicationStatus(applicationId, status) {
    const res = await client.patch(`school-applications/${applicationId}`, { status })
    const idx = schoolApplications.value.findIndex(a => a.id === applicationId)
    if (idx >= 0) {
      schoolApplications.value[idx].status = res.data.data.status
      schoolApplications.value[idx].updated_at = new Date().toISOString()
    }
    if (status === 'approved') {
      await fetchSchools()
    }
    return res.data.data
  }

  async function updateStudentApplicationStatus(applicationId, status) {
    const res = await client.patch(`student-applications/${applicationId}`, { status })
    const idx = studentApplications.value.findIndex(a => a.id === applicationId)
    if (idx >= 0) {
      studentApplications.value[idx].status = res.data.data.status
      studentApplications.value[idx].updated_at = new Date().toISOString()
    }
    if (status === 'approved') {
      await fetchStudents()
    }
    return res.data.data
  }

  async function getLeaderboard(type = 'all') {
    const res = await client.get('leaderboard', { params: { type } })
    const data = res.data.data || []
    if (type === 'school') {
      return data.map(item => ({
        school_id: item.school_id,
        school_name: item.school_name,
        avg_score: item.avg_score,
        rating_count: item.rating_count
      }))
    }
    // 默认综合榜
    return data.map(item => ({
      id: item.student_id || item.studentId || item.id,
      student_id: item.student_id || item.id,
      name: item.name,
      school_id: item.school_id,
      school_name: item.school_name,
      grade: item.grade,
      avg_score: item.avg_score,
      rating_count: item.rating_count,
      dominant_rating: item.dominant_rating ?? (item.avg_score ? Math.round(item.avg_score) : 0),
      rank: item.rank
    }))
  }

  return {
    loading,
    loaded,
    error,
    schools,
    students,
    badges,
    studentBadges,
    schoolApplications,
    studentApplications,
    loadInitial,
    fetchStudents,
    fetchStudentById,
    fetchStudentRatings,
    fetchStudentBadges,
    fetchMyRatings,
    submitRating,
    getStudentRatings,
    getMyRatings,
    createSchoolApplication,
    createStudentApplication,
    fetchSchoolApplications,
    fetchStudentApplications,
    getSchoolApplications,
    getStudentApplications,
    updateSchoolApplicationStatus,
    updateStudentApplicationStatus,
    getLeaderboard
  }
})

