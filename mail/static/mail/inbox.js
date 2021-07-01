document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_sent_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

//Utils
const get_emails = async (mailbox) => {
  await fetch(`/emails/${mailbox}`).then((response) => response.json());
};

const archive = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true,
    }),
  });
  load_mailbox('inbox');
};

const unarchive = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false,
    }),
  });
  load_mailbox('inbox');
};

const unread = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: false,
    }),
  });
  load_mailbox('inbox');
};

function compose_email(emailToReply) {
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  console.log(emailToReply);
  if (emailToReply) {
    // Pre-fill values
    replyRecipients = emailToReply.sender;
    if (emailToReply.subject.slice(0, 3) !== 'Re:') {
      var replySubject = `Re: ${emailToReply.subject}`;
    } else {
      var replySubject = emailToReply.subject;
    }
    replyBody =
      `
On ${emailToReply.timestamp} ${emailToReply.sender} wrote: \n` + emailToReply.body;

    document.querySelector('#compose-recipients').value = replyRecipients;
    document.querySelector('#compose-subject').value = replySubject;
    document.querySelector('#compose-body').value = replyBody;
    document.querySelector('#compose-body').autofocus = true;
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  // Listen for Submit button
  const $form = document.querySelector('#compose-form');
  subject: document.querySelector('#compose-recipients').insertAdjacentHTML('afterEnd', "<div id='compose-error'></div>");

  $form.addEventListener('submit', (e) => {
    // POST
    // Prevent default submission
    e.preventDefault();
    $sendButton = document.querySelector('#compose-button');
    $sendButton.disabled = true;
    setTimeout(() => ($sendButton.disabled = false), 500);
    // Post email
    fetch('/emails', {
      method: 'POST',
      // headers: {
      //   'Content-Type': 'application/json;charset=utf-8',
      // },
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
      }),
      credentials: 'include',
    })
      .then((response) => response.json())
      .then((result) => {
        // Process response result
        if (result.error) {
          // compose-recipients
          $error = `<p id="error">${result.error}</p>`;
          document.querySelector('#compose-error').innerHTML = $error;
          $error = '';
          console.log(result);
        }
        // Print result
        else {
          // successModal = document.createElement('div');
          // successModal = document.createElement('div').innerHTML = '<h2>Sent successfully</h2><p>You will be redirected to your Sent mailbox in 3 second.</p>';

          // document.querySelector('#compose-view').innerHTML = '<h2>Sent successfully</h2><p>You will be redirected to your Sent mailbox in 3 second.</p>';
          setTimeout(() => {
            load_sent_mailbox('sent');
          }, 1000);
        }
        // load_sent_mailbox('sent');
      })
      // Catch any errors and log them to the console
      .catch((error) => {
        console.log('Error:', error);
      });
    // Prevent default submission
    // return false;
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Check if emails list is not empty:
      if (emails.length > 0) {
        // Work with emails

        // Create table element
        const $table = document.createElement('table');
        $table.classList.add('table', 'table-striped', 'table-sm');
        const $divTable = document.createElement('div');
        $divTable.classList.add('table-responsive');

        //Creating heading for emails table

        $heading = document.createElement('tr');
        $heading.innerHTML = "<th id='from'>From</th><th id='topic'>Topic</th><th id='date'>Date</th>";
        $table.append($heading);

        // $table.insertAdjacentHTML('afterbegin', $heading);

        // Go via emails
        emails.forEach((email) => {
          // const mail_element = document.createElement('div');
          // mail_element.innerHTML = `Sender: ${email.sender}, Topic: ${email.subject}`;
          // mail_element.innerHTML = `<div style="display:inline-block">${email.sender}, Topic: ${email.subject}`;
          $row = document.createElement('tr');
          $row.innerHTML = `<td>${email.sender}</td><td>${email.subject}</td><td>${email.timestamp}</td>`;
          $row.style.cursor = 'pointer';
          $row.onmouseover = function () {
            $row.style.border = '1px solid black';
          };
          $row.onmouseleave = function () {
            $row.style.opacity = '1';
          };

          if (email.read == true) {
            $row.style.background = '#ededed';
          } else {
            $row.style.background = 'white';
          }
          // var $row = new DOMParser().parseFromString(row, 'text/xml');
          $row.addEventListener('click', function () {
            viewEmail(email.id, mailbox);
          });

          $table.append($row);
          // $table.insertAdjacentHTML('beforeend', $row);
        });

        //
        $divTable.append($table);
        document.querySelector('#emails-view').append($divTable);

        // document.querySelector('#emails-view').append($table);
      } else {
        // Display empty message on the screen
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> is empty`;
      }
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.log('Error:', error);
    });
}

//Separate fucntion due to different structure of the table (field "To" instead of "From")

function load_sent_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Check if emails list is not empty:
      if (emails.length > 0) {
        // Work with emails

        // Create table element
        const $table = document.createElement('table');
        $table.classList.add('table', 'table-striped', 'table-sm');
        // $table.classList.add('table table-striped table-sm');

        //Creating heading for emails table

        $heading = document.createElement('tr');
        $heading.innerHTML = "<th id='to'>To</th><th id='topic'>Topic</th><th id='date'>Date</th>";
        $table.append($heading);

        // Go via emails
        emails.forEach((email) => {
          $row = document.createElement('tr');
          $row.innerHTML = `<td>${email.recipients}</td><td>${email.subject}</td><td>${email.timestamp}</td>`;
          $row.style.background = '#ededed';
          $row.addEventListener('click', function () {
            viewEmail(email.id, mailbox);
          });
          $table.append($row);
        });

        document.querySelector('#emails-view').append($table);
      } else {
        // Display error on the screen
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> is empty`;
      }
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.log('Error:', error);
    });
}

function viewEmail(email_id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Show the email name

  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      // Actions menu for email:
      const $emailMenu = document.createElement('div');

      emailMenuItems = {
        $archive: document.createElement('button'),
        $unarchive: document.createElement('button'),
        $reply: document.createElement('button'),
        $unread: document.createElement('button'),
      };
      for (key in emailMenuItems) {
        emailMenuItems[key].classList.add('btn', 'btn-sm', 'btn-outline-secondary');
      }
      // $emailMenu.append($archive);
      // $emailMenu.append($archive);

      if (mailbox === 'inbox') {
        emailMenuItems.$archive.innerHTML = `<i class='fa fa-archive'></i> Archive`;
        emailMenuItems.$reply.innerHTML = `<i class='fa fa-reply'></i> Reply`;
        emailMenuItems.$unread.innerHTML = `<i class='fa fa-envelope'></i> Mark Unread`;
        $emailMenu.append(emailMenuItems.$archive, emailMenuItems.$reply, emailMenuItems.$unread);
      } else if (mailbox === 'archive') {
        emailMenuItems.$unarchive.innerHTML = 'Unarchive';
        emailMenuItems.$reply.innerHTML = 'Reply';
        emailMenuItems.$unread.innerHTML = 'Mark Unread';
        $emailMenu.append(emailMenuItems.$unarchive, emailMenuItems.$reply, emailMenuItems.$unread);
      }

      // <button class="btn btn-sm btn-outline-primary" id="inbox">Inbox</button>

      // Show email
      document.querySelector('#email-view').innerHTML = ``;
      let $emailHtml = `
      
      <strong>From</strong>: ${email.sender}
      <strong>To</strong>: ${email.recipients}
      <strong>Date</strong>${email.timestamp}
      <hr>
      <h3>${email.subject}</h3>
      <div>${email.body}</div>
      `;

      // put email template to div
      const $div = document.createElement('div');
      $div.innerHTML = $emailHtml;
      $div.classList.add('view-email', 'card-body');

      //add menu and email to email_view

      document.querySelector('#email-view').append($emailMenu);
      document.querySelector('#email-view').append($div);

      // change read status

      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true,
        }),
      });

      // Use menu to make actions;

      emailMenuItems.$archive.addEventListener('click', () => archive(email_id));
      emailMenuItems.$unarchive.addEventListener('click', () => unarchive(email_id));
      emailMenuItems.$reply.addEventListener('click', () => compose_email(email));
      emailMenuItems.$unread.addEventListener('click', () => unread(email_id));
    })
    .catch((error) => {
      console.log('Error:', error);
    });
}

//creates DOM element based on tag and class name
// const createElement = (tag, className) => {
//   const $tag = document.createElement(tag);
//   if (className) {
//     $tag.classList.add(className);
//   }
//   return $tag;
// };
