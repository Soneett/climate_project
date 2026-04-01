import React, { useState } from "react";
import PropTypes from "prop-types";
import IndicatorButton from "../IndicatorButton/IndicatorButton";
import { SUBJECT_INDICATORS, OBJECT_INDICATORS } from "../../constants/relationsConfig";
import styles from "./RelationsSubBar.module.scss";

const RelationsSubBar = ({ onSelectionChange = () => {} }) => {
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

  const getSubjectState = (subjectId) => {
    if (selectedSubject === subjectId) return 'selected';
    if (selectedObject) {
      const objectConfig = OBJECT_INDICATORS.find(o => o.id === selectedObject);
      if (objectConfig && !objectConfig.availableSubjects.includes(subjectId)) return 'disabled';
    }
    return 'default';
  };

  const getObjectState = (objectId) => {
    if (selectedObject === objectId) return 'selected';
    if (selectedSubject) {
      const subjectConfig = SUBJECT_INDICATORS.find(s => s.id === selectedSubject);
      if (subjectConfig && !subjectConfig.availableObjects.includes(objectId)) return 'disabled';
    }
    return 'default';
  };

  const handleSubjectClick = (subjectId) => {
    const state = getSubjectState(subjectId);
    if (state === 'disabled') return;

    if (selectedSubject === subjectId) {

      setSelectedSubject(null);
      onSelectionChange(null, selectedObject);
    } else {

      setSelectedSubject(subjectId);

      const subjectConfig = SUBJECT_INDICATORS.find(s => s.id === subjectId);
      if (selectedObject && subjectConfig && !subjectConfig.availableObjects.includes(selectedObject)) {
        setSelectedObject(null);
        onSelectionChange(subjectId, null);
      } else {
        onSelectionChange(subjectId, selectedObject);
      }
    }
  };

  const handleObjectClick = (objectId) => {
    const state = getObjectState(objectId);
    if (state === 'disabled') return;

    if (selectedObject === objectId) {

      setSelectedObject(null);
      onSelectionChange(selectedSubject, null);
    } else {

      setSelectedObject(objectId);

      const objectConfig = OBJECT_INDICATORS.find(o => o.id === objectId);
      if (selectedSubject && objectConfig && !objectConfig.availableSubjects.includes(selectedSubject)) {
        setSelectedSubject(null);
        onSelectionChange(null, objectId);
      } else {
        onSelectionChange(selectedSubject, objectId);
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.inner}>
        <div className={styles.column}>
          <h3 className={styles.columnTitle}>Показатель субъект</h3>
          <div className={styles.buttonList}>
            {SUBJECT_INDICATORS.map((subject) => (
              <IndicatorButton
                key={subject.id}
                label={subject.label}
                state={getSubjectState(subject.id)}
                onClick={() => handleSubjectClick(subject.id)}
                size="medium"
              />
            ))}
          </div>
        </div>

        <div className={styles.column}>
          <h3 className={styles.columnTitle}>Показатель объект</h3>
          <div className={styles.buttonList}>
            {OBJECT_INDICATORS.map((object) => (
              <IndicatorButton
                key={object.id}
                label={object.label}
                state={getObjectState(object.id)}
                onClick={() => handleObjectClick(object.id)}
                size="small"
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

RelationsSubBar.propTypes = {
  onSelectionChange: PropTypes.func
};

export default RelationsSubBar;
