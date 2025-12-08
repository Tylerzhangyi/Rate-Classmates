import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
  // 模拟学校数据
  const schools = ref([
    { id: '1', school_name: '北京大学', created_at: '2024-01-01' },
    { id: '2', school_name: '清华大学', created_at: '2024-01-01' },
    { id: '3', school_name: '复旦大学', created_at: '2024-01-01' },
    { id: '4', school_name: '上海交通大学', created_at: '2024-01-01' }
  ])

  // 模拟学生数据
  const students = ref([
    {
      id: '1',
      school_id: '1',
      school_name: '北京大学',
      name: '张三',
      grade: 2021,
      class_no: 1,
      avg_score: 4.5,
      rating_count: 20,
      dominant_rating: 5
    },
    {
      id: '2',
      school_id: '1',
      school_name: '北京大学',
      name: '王五',
      grade: 2021,
      class_no: 1,
      avg_score: 4.2,
      rating_count: 15,
      dominant_rating: 4
    },
    {
      id: '3',
      school_id: '2',
      school_name: '清华大学',
      name: '李四',
      grade: 2022,
      class_no: 2,
      avg_score: 4.8,
      rating_count: 30,
      dominant_rating: 5
    },
    {
      id: '4',
      school_id: '2',
      school_name: '清华大学',
      name: '赵六',
      grade: 2022,
      class_no: 3,
      avg_score: 3.5,
      rating_count: 10,
      dominant_rating: 3
    },
    {
      id: '5',
      school_id: '3',
      school_name: '复旦大学',
      name: '孙七',
      grade: 2023,
      class_no: 1,
      avg_score: 4.0,
      rating_count: 18,
      dominant_rating: 4
    }
  ])

  // 模拟评分数据
  const ratings = ref([
    {
      id: '1',
      rater_id: '2',
      rater_name: '李四',
      target_id: '1',
      target_name: '张三',
      score: 5,
      comment: '非常优秀的同学，学习认真，乐于助人！',
      created_at: '2024-01-15T10:00:00Z'
    },
    {
      id: '2',
      rater_id: '1',
      rater_name: '张三',
      target_id: '2',
      target_name: '王五',
      score: 4,
      comment: '人很好，很友善',
      created_at: '2024-01-16T14:30:00Z'
    }
  ])

  // 模拟徽章数据
  const badges = ref([
    {
      id: '1',
      name: '年度最受欢迎同学',
      description: '获得最多好评的同学',
      badge_type: 'student',
      rule_desc: '评分数量最多'
    },
    {
      id: '2',
      name: '最佳学习伙伴',
      description: '学习能力最强的同学',
      badge_type: 'student',
      rule_desc: '平均分最高'
    },
    {
      id: '3',
      name: '最友善学校',
      description: '整体评分最高的学校',
      badge_type: 'school',
      rule_desc: '学校平均分最高'
    }
  ])

  // 模拟学生徽章
  const studentBadges = ref([
    {
      id: '1',
      student_id: '1',
      badge_id: '1',
      badge_name: '年度最受欢迎同学',
      period: '2024-Q1',
      awarded_at: '2024-01-20T10:00:00Z'
    },
    {
      id: '2',
      student_id: '3',
      badge_id: '2',
      badge_name: '最佳学习伙伴',
      period: '2024-Q1',
      awarded_at: '2024-01-20T10:00:00Z'
    }
  ])

  // 模拟学校申请数据
  const schoolApplications = ref([
    {
      id: '1',
      applicant_id: '1',
      applicant_name: '张三',
      applicant_account: 'student001',
      school_name: '浙江大学',
      contact: 'zhangsan@example.com',
      reason: '希望添加我们学校',
      status: 'pending',
      created_at: '2024-01-25T10:00:00Z'
    }
  ])

  // 添加评分
  function addRating(rating) {
    const newRating = {
      id: String(ratings.value.length + 1),
      ...rating,
      created_at: new Date().toISOString()
    }
    ratings.value.push(newRating)
    
    // 更新学生统计
    const student = students.value.find(s => s.id === rating.target_id)
    if (student) {
      const existingRatings = ratings.value.filter(r => r.target_id === rating.target_id)
      student.rating_count = existingRatings.length
      student.avg_score = (
        existingRatings.reduce((sum, r) => sum + r.score, 0) / existingRatings.length
      ).toFixed(2)
      
      // 计算出现最多的等级
      const scoreCounts = {}
      existingRatings.forEach(r => {
        scoreCounts[r.score] = (scoreCounts[r.score] || 0) + 1
      })
      student.dominant_rating = parseInt(
        Object.keys(scoreCounts).reduce((a, b) => scoreCounts[a] > scoreCounts[b] ? a : b)
      )
    }
    
    return newRating
  }

  // 添加学生
  function addStudent(student) {
    const newStudent = {
      id: String(students.value.length + 1),
      ...student,
      avg_score: 0,
      rating_count: 0,
      dominant_rating: 0
    }
    students.value.push(newStudent)
    return newStudent
  }

  // 添加学校
  function addSchool(school) {
    const newSchool = {
      id: String(schools.value.length + 1),
      ...school,
      created_at: new Date().toISOString()
    }
    schools.value.push(newSchool)
    return newSchool
  }

  // 获取学生的所有评分
  function getStudentRatings(studentId) {
    return ratings.value.filter(r => r.target_id === studentId)
  }

  // 添加学校申请
  function addSchoolApplication(application) {
    const newApplication = {
      id: String(schoolApplications.value.length + 1),
      ...application,
      created_at: new Date().toISOString()
    }
    schoolApplications.value.push(newApplication)
    return newApplication
  }

  // 获取学校申请列表
  function getSchoolApplications(status = null) {
    if (status) {
      return schoolApplications.value.filter(app => app.status === status)
    }
    return schoolApplications.value
  }

  // 更新学校申请状态
  function updateSchoolApplicationStatus(applicationId, status) {
    const application = schoolApplications.value.find(app => app.id === applicationId)
    if (application) {
      application.status = status
      application.updated_at = new Date().toISOString()
      
      // 如果审核通过，自动添加学校
      if (status === 'approved') {
        addSchool({
          school_name: application.school_name
        })
      }
      return application
    }
    return null
  }

  // 获取排行榜数据
  function getLeaderboard(type = 'all', period = 'all') {
    let filtered = [...students.value]
    
    if (type === 'school') {
      // 按学校分组计算平均分
      const schoolMap = {}
      students.value.forEach(s => {
        if (!schoolMap[s.school_id]) {
          schoolMap[s.school_id] = {
            school_id: s.school_id,
            school_name: s.school_name,
            students: [],
            total_score: 0,
            total_count: 0
          }
        }
        schoolMap[s.school_id].students.push(s)
        schoolMap[s.school_id].total_score += s.avg_score * s.rating_count
        schoolMap[s.school_id].total_count += s.rating_count
      })
      
      return Object.values(schoolMap)
        .map(school => ({
          ...school,
          avg_score: school.total_count > 0 
            ? (school.total_score / school.total_count).toFixed(2) 
            : 0
        }))
        .sort((a, b) => parseFloat(b.avg_score) - parseFloat(a.avg_score))
        .slice(0, 10)
    }
    
    // 综合榜
    return filtered
      .filter(s => s.rating_count > 0)
      .sort((a, b) => parseFloat(b.avg_score) - parseFloat(a.avg_score))
      .slice(0, 10)
      .map((s, index) => ({
        ...s,
        rank: index + 1
      }))
  }

  return {
    schools,
    students,
    ratings,
    badges,
    studentBadges,
    schoolApplications,
    addRating,
    addStudent,
    addSchool,
    addSchoolApplication,
    getSchoolApplications,
    updateSchoolApplicationStatus,
    getStudentRatings,
    getLeaderboard
  }
})

