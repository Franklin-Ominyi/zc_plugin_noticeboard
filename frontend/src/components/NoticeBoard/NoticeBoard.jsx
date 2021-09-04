import React from 'react'
import './NoticeBoard.css'
import NoticeBoardHeader from './NoticeBoardHeader'
import AdminNotice from '../NoticeBoard/noticeBoardComponent/AdminNotice'
import { BrowserRouter as  Switch, Route } from "react-router-dom"
// import UserNotice from "../NoticeBoard/noticeBoardComponent/UserNoticeBoard";
import CreateNotice from './noticeBoardComponent/CreateNotice'
import UserIntro from "../NoticeBoard/noticeBoardComponent/UserIntro component/UserIntro"

function NoticeBoard() {
  return (
    <div className="notice">
      <NoticeBoardHeader />
      <Switch>
        <Route path="/create-notice">
          <CreateNotice />
        </Route>
        <Route path="/admin-notice">
          <AdminNotice />
        </Route>

        <Route path="/">
          <UserIntro />
        </Route>

        {/* <Route path="/">
          this component should be created in the NoticeBoard/noticeBoard folder  remember to create a link for the View Notice Button that routes to admin-notice above <UserNotice />
        </Route> */}
      </Switch>
    </div>
  );
}

export default NoticeBoard;
